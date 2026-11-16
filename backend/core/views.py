import io
import json
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET
from django.middleware.csrf import get_token
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
)
from core.permissions import member
from core.idempotency import execute
from core.validation import scoped, text, provenance
from core.models import AuditEvent, Incident
from organizations.models import Institution, Membership, Site, Area
from catalog.models import Material
from waste.models import Generation
from traceability.models import Lot
from compost.models import Process, Evidence
from waste import services as waste
from traceability import services as trace
from compost import services as compost
from reports.selectors import report
from reports.observatory import observatory
from traceability.passport import passport
from reports.scenarios import preview
from reports.csv_export import export


@ensure_csrf_cookie
@require_GET
def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


@csrf_protect
@require_POST
def sign_in(request):
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse({"message": "Solicitud inválida."}, status=400)
    if not isinstance(data, dict) or not all(
        isinstance(data.get(k), str) and 0 < len(data[k]) <= 150
        for k in ["username", "password"]
    ):
        return JsonResponse({"message": "Usuario y contraseña requeridos."}, status=400)
    user = authenticate(
        request, username=data.get("username"), password=data.get("password")
    )
    if (
        not user
        or not Membership.objects.filter(user=user, institution__active=True).exists()
    ):
        return JsonResponse({"message": "Credenciales inválidas."}, status=401)
    login(request, user)
    return JsonResponse({"username": user.username, "role": user.membership.role})


def audit(m, entity, reason, before=None, after=None):
    AuditEvent.objects.create(
        institution=m.institution,
        actor=m.user,
        entity=entity,
        reason=reason,
        before=before or {},
        after=after or {},
    )


def institution_data(m, resource):
    if resource == "institution":
        return {"id": m.institution.id, "name": m.institution.name}
    if resource == "users":
        if m.role != "administrador":
            raise PermissionDenied()
        return [
            {
                "id": x.user_id,
                "username": x.user.username,
                "role": x.role,
                "active": x.user.is_active,
            }
            for x in Membership.objects.filter(
                institution=m.institution
            ).select_related("user")
        ]
    model = {"sites": Site, "areas": Area, "materials": Material}[resource]
    return list(model.objects.filter(institution=m.institution).values())


def configure(m, resource, data, pk=None):
    if resource == "users":
        role = data.get("role")
        if role not in ["administrador", "gestor", "operador", "consultor"]:
            raise ValidationError("Rol inválido.")
        if pk:
            membership = get_object_or_404(
                Membership, institution=m.institution, user_id=pk
            )
            if membership.user_id == m.user_id:
                raise ValidationError("No puedes cambiar tu propio rol.")
            before = {"role": membership.role}
            membership.role = role
            membership.save(update_fields=["role"])
            user = membership.user
        else:
            username = text(data, "username")
            if User.objects.filter(username=username).exists():
                raise ValidationError("Usuario ya existe.")
            password = text(data, "password", 128)
            validate_password(password)
            user = User.objects.create_user(username=username, password=password)
            membership = Membership.objects.create(
                institution=m.institution, user=user, role=role
            )
            before = {}
        audit(m, f"user:{user.id}", "Administración de rol", before, {"role": role})
        return {"id": user.id, "username": user.username, "role": role}
    if resource == "institution":
        m.institution.name = text(data, "name")
        m.institution.save(update_fields=["name"])
        return institution_data(m, resource)
    model = {"sites": Site, "areas": Area, "materials": Material}[resource]
    obj = scoped(model, m, pk, True) if pk else model(institution=m.institution)
    obj.name = text(data, "name")
    if resource == "areas":
        obj.site = scoped(Site, m, data.get("site"))
    if resource == "materials":
        category = data.get("category")
        if category not in ["blanco", "verde", "negro", "especial"]:
            raise ValidationError("Categoría inválida.")
        if (
            pk
            and Generation.objects.filter(material=obj).exists()
            and category != obj.category
        ):
            raise ValidationError("No cambiar categoría utilizada; crea otro material.")
        obj.category = category
        obj.active = data.get("active", True) is True
    obj.full_clean()
    obj.save()
    audit(m, f"{resource}:{obj.pk}", "Configuración institucional")
    return {"id": obj.pk, "name": obj.name}


@api_view(["GET", "POST", "PATCH"])
def dispatch(request, path):
    routes = {
        "GET": r"v2/lots/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/passport|session/me|institution|sites|areas|materials|users|generations(?:/\d+)?|lots(?:/\d+(?:/image)?|/qr/[0-9a-f-]+)?|compost/processes(?:/\d+)?|evidence/\d+/download|incidents|dashboard|observatory|reports/generation\.csv",
        "POST": r"v2/scenarios/preview|session/logout|sites|areas|materials|users|generations(?:/\d+/(?:review|correct))?|lots(?:/\d+/(?:movements|close))?|compost/processes(?:/\d+/(?:inputs|measurements|finalize|evidence|verify))?|incidents",
        "PATCH": r"institution|(?:sites|areas|materials|users)/\d+",
    }
    if not re.fullmatch(routes[request.method], path):
        raise NotFound()
    parts = path.strip("/").split("/")
    resource = parts[0]
    m = member(request)
    data = request.data
    if request.method != "GET" and not isinstance(data, dict):
        raise ValidationError("Se requiere un objeto de datos.")
    if request.method == "GET":
        if resource == "v2":
            return Response(passport(m, parts[2]))
        if path == "session/me":
            return Response(
                {
                    "username": request.user.username,
                    "role": m.role,
                    "institution": m.institution.name,
                }
            )
        if resource in ["institution", "sites", "areas", "materials", "users"]:
            return Response(institution_data(m, resource))
        if resource == "generations":
            query = (
                Generation.objects.filter(institution=m.institution)
                .select_related("area", "material", "actor")
                .order_by("-id")
            )
            if len(parts) > 1:
                g = scoped(Generation, m, parts[1])
                return Response(
                    {
                        **waste.serialize(g),
                        "audit": list(
                            AuditEvent.objects.filter(
                                institution=m.institution, entity=f"generation:{g.id}"
                            ).values()
                        ),
                    }
                )
            # Shared report filtering ensures matching date, area, material and provenance semantics.
            _, rows = report(m, request.query_params)
            ids = {r["id"] for r in rows}
            return Response([waste.serialize(g) for g in query if g.id in ids])
        if resource == "lots":
            if len(parts) > 1:
                if parts[1] == "qr":
                    lot = get_object_or_404(
                        Lot, institution=m.institution, public_id=parts[2]
                    )
                else:
                    lot = scoped(Lot, m, parts[1])
                if parts[-1] == "image":
                    import qrcode
                    from django.conf import settings

                    image = qrcode.make(f"{settings.APP_ORIGIN}/lotes/{lot.public_id}")
                    stream = io.BytesIO()
                    image.save(stream, format="PNG")
                    stream.seek(0)
                    return FileResponse(stream, content_type="image/png")
                return Response(trace.serialize(lot, True))
            return Response(
                [
                    trace.serialize(l, True)
                    for l in Lot.objects.filter(institution=m.institution).order_by(
                        "-id"
                    )
                ]
            )
        if resource == "compost":
            if len(parts) > 2:
                return Response(compost.serialize(scoped(Process, m, parts[2])))
            return Response(
                [
                    compost.serialize(p)
                    for p in Process.objects.filter(institution=m.institution).order_by(
                        "-id"
                    )
                ]
            )
        if resource == "evidence":
            e = scoped(Evidence, m, parts[1])
            if not e.file:
                raise NotFound()
            return FileResponse(e.file.open("rb"), as_attachment=True)
        if resource == "incidents":
            return Response(
                list(
                    Incident.objects.filter(institution=m.institution).values(
                        "id", "entity", "reason", "state", "created_at"
                    )
                )
            )
        if resource == "observatory":
            return Response(observatory(m, request.query_params))
        if resource == "dashboard":
            return Response(report(m, request.query_params, include_rows=False)[0])
        if resource == "reports":
            return export(*report(m, request.query_params))
        raise NotFound()
    if path == "v2/scenarios/preview":
        return Response(preview(m, data))
    if path == "session/logout":
        logout(request)
        return Response({"message": "Sesión cerrada."})
    if resource in ["institution", "sites", "areas", "materials", "users"]:
        m = member(request, ["administrador"])
        if resource == "institution" and request.method != "PATCH":
            raise ValidationError("Solo actualizar el piloto.")
        with transaction.atomic():
            return Response(
                configure(m, resource, data, parts[1] if len(parts) > 1 else None),
                status=200 if request.method == "PATCH" else 201,
            )
    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    # Role check precedes idempotency replay to enforce current authorizations.
    action = parts[-1]
    roles = ["gestor"] if action in ["correct", "review", "verify"] else ["operador"]
    if action == "evidence":
        roles = ["operador", "gestor"]
    if resource == "incidents":
        roles = ["administrador", "operador", "gestor"]
    m = member(request, roles)

    def mutate():
        if resource == "generations":
            if len(parts) == 1:
                return waste.create(m, data)
            if action == "correct":
                return waste.correct(m, parts[1], data)
            if action == "review":
                g = scoped(Generation, m, parts[1], True)
                g.reviewed = True
                g.save(update_fields=["reviewed"])
                audit(m, f"generation:{g.pk}", "Revisión de clasificación")
                return waste.serialize(g)
        if resource == "lots":
            if len(parts) == 1:
                return trace.create(m, data)
            if action == "movements":
                return trace.move(m, parts[1], data)
            if action == "close":
                return trace.close(m, parts[1])
        if resource == "compost":
            if len(parts) == 2:
                return compost.create(m, data)
            fn = {
                "inputs": compost.add_input,
                "finalize": compost.finalize,
                "verify": compost.verify,
                "measurements": compost.measurement,
            }.get(action)
            if fn:
                return fn(m, parts[2], data)
            if action == "evidence":
                return compost.evidence(m, parts[2], data, request.FILES.get("file"))
        if resource == "incidents":
            entity = text(data, "entity", 100)
            try:
                kind, pk = entity.split(":")
            except ValueError:
                raise ValidationError("Referencia inválida.")
            model = {"generation": Generation, "lot": Lot, "process": Process}.get(kind)
            if not model:
                raise ValidationError("Referencia inválida.")
            scoped(model, m, pk)
            x = Incident.objects.create(
                institution=m.institution,
                entity=entity,
                reason=text(data, "reason", 2000),
                actor=m.user,
            )
            return {"id": x.id, "state": x.state}
        raise NotFound()

    # Uploads have content fingerprints; never serialize raw bytes or private data to logs.
    payload = dict(data) if request.FILES else data
    if request.FILES:
        import hashlib

        if (
            resource != "compost"
            or action != "evidence"
            or set(request.FILES) != {"file"}
            or len(request.FILES.getlist("file")) != 1
        ):
            raise ValidationError(
                "Adjunta un único documento en el campo file de evidencia."
            )
        upload = request.FILES["file"]
        if upload.size > 10 * 1024 * 1024:
            raise ValidationError("Máximo 10 MiB.")
        payload = {k: str(v) for k, v in data.items() if k != "file"}
        payload["file_digest"] = hashlib.sha256(upload.read()).hexdigest()
        upload.seek(0)
    result = execute(m, path, request.headers.get("Idempotency-Key"), payload, mutate)
    return Response(result, status=201)

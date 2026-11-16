import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from organizations.models import Institution, Membership, Site, Area
from catalog.models import Material


class Command(BaseCommand):
    help = "Prepara cuentas y catálogo de demostración; no inventa mediciones."

    @transaction.atomic
    def handle(self, *args, **options):
        password = os.getenv("DEMO_PASSWORD")
        if not password or len(password) < 12:
            raise CommandError(
                "Configura DEMO_PASSWORD local de al menos 12 caracteres."
            )
        institution, _ = Institution.objects.get_or_create(
            name="Universidad piloto · DEMOSTRACIÓN"
        )
        site, _ = Site.objects.get_or_create(
            institution=institution, name="Campus demostrativo"
        )
        Area.objects.get_or_create(institution=institution, site=site, name="Cafetería")
        for name, category in [
            ("Orgánicos de cafetería", "verde"),
            ("Papel y cartón", "blanco"),
            ("Residuos no aprovechables", "negro"),
        ]:
            Material.objects.get_or_create(
                institution=institution, name=name, defaults={"category": category}
            )
        for role in ["administrador", "operador", "gestor", "consultor"]:
            user, created = User.objects.get_or_create(username="demo_" + role)
            if created:
                user.set_password(password)
                user.save()
                Membership.objects.create(user=user, institution=institution, role=role)
            elif not Membership.objects.filter(
                user=user, institution=institution, role=role
            ).exists():
                raise CommandError(
                    "Nombre de usuario existente ajeno a demo; no se modificó."
                )
        self.stdout.write(
            self.style.SUCCESS(
                "Demo preparada. Usuarios demo_administrador, demo_operador, demo_gestor, demo_consultor. Contraseña en .env local; no se imprime."
            )
        )

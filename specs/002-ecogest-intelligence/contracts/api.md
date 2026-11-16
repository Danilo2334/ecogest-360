# Contratos V2

## Fase A autorizada

GET /api/observatory, sesión institucional y permisos de lectura de los cuatro roles.
Filtros V1: generated_from/to, area, material, provenance, cutoff. Mismos errores 400/401/403;
referencias de otra institución no revelan registros. Sin POST nuevo.
Respuesta: summary (report V1 con rate=null si mezcla), comparison {available,reason,current_from,
current_to,previous_from,previous_to,previous_generated,absolute,percent}, series [{date,kg,count}],
areas [{id,name,generated,pending}], provenance_totals [{provenance,generated}], insights [{code,title,detail}],
context {cutoff,coverage,series_reason}. Todos los kg son cadenas decimales, no floats.
Comparación requiere procedencia única, ambos extremos, hasta ayer Bogotá, duración ≤366 días.
Anterior inmediatamente previo con duración igual; si una cohorte no tiene registros no compara;
si denominador anterior cero, porcentaje null. Corte debe cubrir fin de ambos períodos para comparar.
Serie solo días presentes, tabla/nota explican huecos; intervalo demasiado amplio devuelve motivo,
no trunca silenciosamente. Ranking de todas las áreas contribuyentes, sorted -generated/name/id.
Fórmulas y fuente V1 conservadas; mezcla no ofrece porcentaje conjunto. CSV V1 intacto.

## Interfaces futuras (no implementar en A)

B GET /api/v2/lots/{uuid}/passport: proyección de fuentes/eventos/evidencias autenticada.
C POST /api/v2/scenarios/preview: CSRF; cálculo puro, hipótesis enum reducción/aumento_acreditación,
importe decimal no negativo, base revalidada por servidor, 409 si obsoleta. Sin persistencia.
D GET/POST /api/v2/plans; PATCH /api/v2/plans/{id}; POST /transitions y /evaluations:
solo gestor escribe, versión esperada, motivo obligatorio; lecturas institucionales.
E POST /api/v2/assistant: modo, pregunta, filtros; contexto recalculado por servidor,
resultado estructurado con cifras/fuentes verificadas y estado disponible/no_disponible.
No herramientas mutadoras. Cuota agotada 429, falta configuración estado no_disponible.
Contratos detallados de fases B–E se revisarán antes de autorizar cada implementación.
# Adenda de refinamiento A

GET observatory: los elementos de insights añaden `interpretation` y `suggestion` (texto),
y `area` (ID opcional para evidencia filtrada). El hallazgo largest_area describe masa absoluta;
no normaliza por ocupación. Todos los demás filtros se conservan al abrir sus registros.
Los KPI abren la cohorte base, no un subconjunto supuestamente acreditado. Balance y materiales
usan summary.generated/verified_compost/pending/distribution, sin alterar report/dashboard/CSV V1.
El comando de demostración no crea endpoints ni amplía permisos de API.


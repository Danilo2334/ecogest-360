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



## B — contrato autorizado
GET /api/v2/lots/{uuid}/passport devuelve lot {id,public_id,provenance,state}, balance
{assigned,available,consumed}, sources con generación/material/área/masa asignada, events
{key,kind,date,actor,kg,balance_effect,description,process,evidence_url}, processes con
entrada de este lote, entrada total, salida independiente y estado/verificación.
Fechas ISO de registros reales; actor de creación del lote no persistido se declara null.
Eventos de proceso compartido no reparten su salida entre lotes. Autenticación y ámbito
institucional en cada acceso. 404 para ajeno/inexistente, 401 sin sesión. Sin escrituras.

## C — contrato autorizado
POST /api/v2/scenarios/preview: {filters, hypothesis, amount, base_token?}.
filters solo generated_from/to,area,material,provenance; corte manual no permitido porque E
es disponibilidad actual. Procedencia única y período obligatorio. Hipótesis increase_compost
o reduce_nonrecoverable; amount decimal 0..límite, hasta 3 decimales.
Respuesta base (report vigente), eligible E, nonrecoverable N, base_token (huella sin corte
volátil), result {generated,verified_compost,pending,rate}, delta (kg y puntos de tasa),
filters, formula, limitations. La primera carga usa amount=0; cálculos posteriores envían
base_token; si cambió contexto/masas/elegibilidad, 409 y recarga explícita.
Ninguna operación idempotente ni registro persistido para simulación: cálculo puro, sesión y
CSRF exigidos. No ofrece interpretación de saldo pasado ni acredita estimados.

## D — contrato detallado de implementación
GET /api/v2/plans lista institucional y /api/v2/plan-options miembros activos autorizados
para asignación (solo identidad local, nunca contexto IA). POST /api/v2/plans crea borrador
con problem,action,area,responsible,indicator (generated/verified_compost/rate), target,
direction (reduce/increase), due_date, filters, reason. Gestor único escritor.
PATCH /api/v2/plans/{id}: version y reason obligatorios; campos editables problem/action/
responsible/target/direction/due_date; no sustituir universo/área/indicador/base.
POST /api/v2/plans/{id}/transitions: version,reason,state; borrador→en_curso→en_evaluacion→
cerrado; cancelar desde cualquier estado no terminal con motivo. Inicio captura base
actual congelada; cierre exige evaluación persistida. Estados terminales no editables.
POST /api/v2/plans/{id}/followups: version,reason,text; seguimiento humano auditable.
POST /api/v2/plans/{id}/evaluations: version,reason,generated_from/to.
El período base y posterior deben estar cerrados, tener igual duración, sin solapamiento
y conservar procedencia/área/material. El corte lo fija el servidor al evaluar; cohortes
con distinta maduración se advierten. Sin datos, tasa nula o fuente base corregida: no_evaluable.
La evaluación recalcula fuente base y la compara con su huella excluyendo el corte volátil,
pero incluyendo generación, acreditación e IDs/valores fuente. Resultado persistido
con valor, meta vigente, filtros y motivo; nunca afirma causalidad. Cambio de meta posterior
invalida evaluación previa para cierre (debe evaluar de nuevo).
PlanRevision registra antes/después y actor por cada cambio; bloqueo fila + version contra
sobrescritura concurrente, idempotencia para POST mutadores mediante mecanismo existente.
Decimales no negativos hasta 3 posiciones; tasa objetivo 0..100; fechas ISO válidas;
textos no vacíos hasta 2000; responsable activo de misma institución; sin DELETE.

## E — contrato de implementación controlada
GET /api/v2/assistant/context?{filtros}: hechos locales, metodología y disponibilidad sin llamar IA.
POST /api/v2/assistant: {mode: mis_datos|explicar|proponer, question: 1..2000,
filters: generated_from/to,provenance,area?,material?,cutoff?}, Idempotency-Key UUID.
No campos extra (incluidos institution_id, contexto, SQL o herramientas). Procedencia única.
Sesión y CSRF; todos los roles leen su institución. No recibe historial conversacional.
Devuelve status, reason, facts, explanations, actions, context, answer (null si degradado).
El proveedor selecciona IDs de hechos y códigos de explicaciones/acciones de un catálogo
determinista. La redacción factual y las cifras se renderizan desde ese catálogo; no se
publica texto libre del modelo. Así se verifican también referencias y ausencia de cifras
inventadas, sin fingir una respuesta abierta universal. Fuera de ese alcance: insufficient.
El contexto externo omite nombres de usuarios/instituciones, textos libres y adjuntos;
áreas se representan con IDs, nombres se resuelven solo localmente. Máximo 6000 bytes de
contexto (cota conservadora de tokens) y 16000 bytes entrada completa + esquema; 1000 tokens
de salida. No tools, previous_response_id, búsquedas ni SQL. store=false, timeout 25 s,
sin reintentos SDK. Detectar patrones obvios de secretos/correo en pregunta; advertir al
usuario no ingresar información privada (no garantiza anonimización universal).
Uso externo bloqueado salvo AI_ENABLED, AI_BUDGET_AUTHORIZED y OPENAI_SMOKE_TEST=1,
clave presente, modelo tarifado permitido y presupuestos diario institucional/proyecto >0.
Reserva atómica previa con advisory lock global; un envío pendiente por usuario, cinco
intentos/minuto; UUID repetido 409 sin repetir gasto. No persistir preguntas/respuestas.
Metadatos de uso conservan costo reservado/consumido; errores sin usage retienen reserva
conservadora. Un proceso interrumpido requiere conciliación administrativa, nunca liberar
cuota automáticamente si el cobro es incierto. 429 límites. Errores del proveedor: estado
no_disponible sin detalles técnicos/secretos. Solo esta tabla técnica cambia al consultar.

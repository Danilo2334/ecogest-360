# Modelo de datos V2

## A — solo proyecciones, sin migraciones

Generation, Allocation, ConsumptionSource, Process, Verification y Area conservan esquema V1.
ObservatoryContext: filtros, corte ISO, procedencia y períodos; no persistente.
Serie: fecha local, kg (cadena 3 decimales), número de registros. Ausencia no es medición cero.
Ranking: area_id, nombre, kg generados, pendiente; identidad por ID, desempate nombre/ID.
Hallazgo: código determinista, texto, valores, filtros fuente; no entidad ambiental nueva.

## B/C — proyecciones implementadas

Pasaporte es proyección de lotes y relaciones, sin nueva masa. Escenario vive en memoria:
base, corte, hipótesis única, E/N, resultado; no tablas ni escrituras operativas.

## D — persistencia aditiva

InterventionPlan: institución/creador, problema y acción (1–2000 caracteres), área y responsable
activos de la misma institución; indicador enum generación/compostaje_acreditado/tasa, unidad kg/%;
meta decimal y dirección reducir/aumentar, fecha objetivo, base JSON inmutable al inicio con
filtros/valor/corte/fuentes, estado borrador/en_curso/en_evaluacion/cerrado/cancelado, versión entera.
PlanRevision: plan, actor, momento, motivo 1–2000, antes/después; append-only.
PlanEvaluation: plan, período posterior, valor, fuentes y resultado alcanzada/no_alcanzada/no_evaluable;
misma duración/procedencia/filtros; no causalidad. Gestor único escritor. Conflicto versión →409.
Transiciones y restricciones: spec FR-017–020; cancelar con motivo, cerrar con evaluación registrada.

## E — contabilidad separada

Conversación efímera, no mensajes persistentes. Cuotas/uso mínimos separados de dominio:
institución, período, presupuesto autorizado, reserva y coste consumido, sin preguntas/respuestas.
Activación requiere precio/modelo y monto aprobados; reserva atómica antes de cada llamada.
Entidad física Invocation: institución/usuario, UUID idempotente, momento/día, modelo,
estado pending/completed/unknown, debit decimal USD y tokens de entrada/salida nullable.
Unique usuario+UUID y débito no negativo. Los límites autorizados se leen del entorno;
consumo agregado institucional diario y global acumulado, no se reinicia automáticamente.
Reservas inciertas permanecen contabilizadas. Sin tabla de conversaciones ni contenido
en OperationReceipt. Followup de Plan registra avance humano sin alterar la base ambiental.

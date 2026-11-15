# Modelo de datos propuesto

Documento de diseño, sin modelos implementados ni migraciones ejecutadas.

## Convenciones

Todas las entidades ambientales tienen institución, identificador, creado_en y creado_por.
Relaciones entre instituciones diferentes se rechazan en los servicios. El borrado de referencias
ambientales usa protección. Fechas con zona; almacenar UTC y presentar America/Bogota.
Masa: **Decimal(12,3), mayor que cero; saldo mayor o igual que cero**. Sin float ni redondeo
silencioso. Campos de identidad externos son UUID; no constituyen autorización.
Campos no señalados como opcionales son obligatorios. Límites técnicos se validan también
en entrada. Nombres: **1–150 caracteres**; motivos: **1–2000 caracteres**.

## Entidades y relaciones

| Entidad | Atributos y relaciones | Restricciones |
| --- | --- | --- |
| Institution | nombre, activa | Una institución administrable en piloto |
| Site / Area | nombre, institución; área pertenece a sede | Referencias activas al capturar; preservar historia |
| Membership | usuario Django, institución, rol | Un rol por usuario e institución; administrador, gestor, operador, consultor |
| Material | nombre, categoría, elegible_compostaje, activo | Categoría: blanco, verde, negro, especial; solo verde elegible; especial no registrable como ordinario |
| Generation | área, material, kg, fecha, procedencia, método, revisado_por opcional, revisión_fecha opcional | Procedencia: medido, estimado, simulado; método obligatorio para medido/estimado; corrección solo sin Allocation |
| Lot | UUID público, procedencia, estado | Estado: abierto, agotado, cerrado; saldo derivado de asignaciones menos consumos |
| Allocation | Generation, Lot, kg | Bloquear Generation al asignar; suma de asignaciones no supera generación |
| Movement | Lot, tipo, kg, destino, fecha, responsable | Tipo: logístico, entrega, entrada_compostaje; logístico no consume saldo; los otros generan un único Consumption |
| Consumption | Lot, Movement, kg, destino_tipo | Movement único; efecto inmutable; referencia única a CompostInput si aplica |
| CompostProcess | procedencia, inicio, estado, observaciones opcionales | Estado: en_proceso, finalizado; entradas solo mientras en_proceso |
| CompostInput | Process, Consumption | Consumption único, misma institución y procedencia, material orgánico |
| Measurement | Process, valor decimal, unidad, fecha, tipo, autor | Opcional; no generada automáticamente |
| CompostOutput | Process, kg, fecha, destino, responsable, procedencia | Un resultado consolidado por proceso; kg independiente, misma procedencia que proceso |
| Evidence | Process, receptor, fecha_destino, descripción, autor, archivo opcional, referencia opcional | Archivo o referencia verificable obligatorio; PDF/JPEG/PNG hasta 10 MiB |
| Verification | Process, gestor, fecha, decisión, motivo | Confirmación única por proceso; rechazos históricos conservados; ninguna confirmación sin requisitos Q3 |
| AuditEvent | entidad, antes, después, motivo, actor, fecha | Inmutable; no almacenar secretos |
| Incident | referencia ambiental, motivo, autor, fecha, estado | Estado: pendiente; no altera entidad ni saldos |
| OperationReceipt | institución, actor, tipo, clave, hash, resultado | Unicidad institución+actor+tipo+clave; se guarda en misma transacción que el efecto |

## Invariantes y operaciones

1. Asignar: bloquear Generation en orden UUID; comprobar kg positivos, institución,
   material/procedencia compatibles y disponible; crear Allocation y Lot juntos.
2. Consumir: bloquear Lot; recalcular saldo desde Allocation y Consumption; verificar estado;
   crear Movement, Consumption y CompostInput cuando corresponda dentro del mismo atomic.
   Si un lote agrupa varios registros, exigir igual material y procedencia; mantener reparto
   de cada consumo a sus Allocation en **ConsumptionSource(consumo, asignación, kg)**.
   Repartir determinísticamente por fecha de origen e ID; sumar exactamente la masa consumida
   sin exceder cada origen. Este reparto hace filtrables las entradas por cohorte y área.
3. Entrada: bloquear proceso antes del lote, con orden global proceso → generación → lote;
   jamás invertir el orden. No aceptar entrada si el proceso está finalizado.
4. Finalizar: bloquear proceso; exigir al menos una entrada y salida independiente positiva;
   registrar destino declarado; bloquear entrada/salida futuras. No implica verificación.
5. Confirmar: bloquear proceso; gestor verifica finalización, entradas, salida, fecha, responsable
   y evidencia del destino de todo el resultado; confirmación única e inmutable. Evitar
   modificación concurrente de evidencia; bloqueo de proceso también al aportar evidencia.
6. Corregir: bloquear Generation; comprobar cero Allocation; validar valores nuevos y guardar
   auditoría en el mismo atomic. Contra carreras con asignación, ambas bloquean Generation.
7. Cerrar lote: saldo cero y ningún proceso relacionado abierto; operador deja evento auditado.
   Una incidencia puede añadirse después, pero no cambia datos cerrados ni resultados confirmados.

## Consultas e índices

Filtrar institución antes de búsqueda por ID y repetir permisos de operación. Índices por
institución/fecha, material, área y referencias de lotes/procesos; restricciones únicas en
consumo, entrada, recibo y confirmación. Evitar joins que multipliquen masa: agregar generación
y consumo por separado, y construir A desde ConsumptionSource validado por proceso.
Los informes no reconstruyen versiones históricas de correcciones; registran este límite.

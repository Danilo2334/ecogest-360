# EcoGest 360 — Alcance funcional propuesto para la primera entrega (MVP SDD)

> Insumo de requisitos para el comando de Spec Kit `$speckit-specify`. **No sustituye** el `spec.md` generado por el flujo SDD. El proyecto completo es más amplio; esta entrega se centra en un recorrido integrado y demostrable.

## Problema y usuarios
Una institución educativa necesita registrar residuos sólidos, conocer su clasificación, seguir lotes y destinos, monitorear aprovechamiento orgánico y presentar indicadores creíbles. Usuarios: administrador, gestor ambiental, operador y consultor de solo lectura.

## Features principales

### 1. Gestión institucional, usuarios y catálogo de residuos
- Autenticación e inicio/cierre de sesión. Rol administrador administra la institución piloto y catálogo; gestor valida movimientos; operador registra; consultor solo visualiza.
- Registrar espacios generadores (ej. cafetería, aulas, oficinas), y consultar materiales/categorías de separación en fuente.
- Un registro solo puede verse y modificarse por usuarios autorizados. Validación de permisos en servidor, no solo ocultar botones.
- Clasificar residuos ordinarios aprovechables, orgánicos aprovechables y no aprovechables según la separación aplicable en Colombia. Los peligrosos y de manejo diferenciado no se ofrecen como residuo ordinario.

### 2. Generación y caracterización
- Registrar fecha, área, tipo de residuo, cantidad positiva en kg, responsable y procedencia `medido | estimado | simulado`.
- Listar, filtrar, consultar detalles y conservar historial de cambios; si se permite rectificar registros validados, registrar motivo y auditoría.
- Rechazar masa cero, negativa o sin unidad. No simular datos silenciosamente para mostrar cifras.

### 3. Lotes, recolección y trazabilidad QR
- Crear un lote desde masa disponible de residuos registrados y asignar identificador único con QR que no contenga secretos.
- Registrar movimientos/entregas con fecha, operador, destino, cantidad y estado; consultas pueden mostrar línea de eventos autorizada.
- **No superar saldo disponible**, ni duplicar movimientos por doble envío o concurrencia; recolección nunca suma nueva generación de residuos.
- No modificar lote cerrado salvo operación de corrección explícita y auditada.

### 4. Aprovechamiento y compostaje
- Permitir iniciar proceso de compostaje con masa orgánica disponible y registrar fecha de inicio, observaciones, mediciones opcionales y estado.
- Registrar resultado de compost obtenido por masa medida independientemente y destino declarado; no presumir equivalencia con masa de entrada.
- Los resultados se clasifican como confirmados o pendientes; no afirmar calidad de abono ni cumplimiento normativo sin evidencia.

### 5. Panel ambiental, filtros y reporte
- Mostrar generación por período/área/tipo, residuos con aprovechamiento confirmado y estado pendiente, con representación gráfica accesible.
- Mostrar denominador, numerador, fórmula y fecha de corte de indicadores; no contar recolecciones como nueva generación ni sumar cohortes incompatibles.
- Filtrar para excluir simulados o estimados al presentar resultados académicos de mediciones reales.
- Exportar al menos CSV correcto y reproducible del conjunto filtrado; PDF es mejora si no compromete pruebas/ejecución.

## Demostración vertical mínima
Un operador registra 25 kg **simulados** de residuos orgánicos de cafetería, crea un lote y registra traslado de 20 kg a compostaje. El saldo disponible es 5 kg. Otro movimiento de 6 kg es rechazado sin alterar registros. Se registra una salida de compost como valor independiente del peso de entrada. El dashboard refleja los registros sin contar doble los movimientos; reportes identifican los datos como simulados.

## Reglas de calidad verificables
- Los formularios exhiben errores claros y accesibles; el backend valida también entradas manipuladas.
- APIs sin sesión no revelan registros; un consultor no puede crear ni alterar entidades.
- Operaciones de saldo son transaccionales y resistentes a doble envío; tests automatizados las cubren.
- Base de datos real y persistente, no mocks como fuente de verdad. Datos de demostración creados mediante procedimiento documentado y marcados como simulados.
- No se registran secretos en repo; `.env.example` contiene solo placeholders. Interfaz responsive y mensajes en español.

## Lo que NO se va a construir en esta iteración (Non-Goals)
- Sensores IoT, pesaje automático, dispositivos embebidos, integración en tiempo real con básculas.
- Mercado o venta de materiales, pagos, gestión integral de cultivos, logística agrícola y certificaciones oficiales.
- Cálculos de huella de carbono certificados, gestión técnica/operativa de residuos peligrosos y dictámenes ambientales automáticos.
- IA por visión de imágenes, chatbot Gemini, pronósticos y recomendaciones autónomas: quedan planificados para una futura iteración, no para bloquear el MVP.
- Multiinstitución desplegada públicamente, apps móviles nativas, colas distribuidas y microservicios.
- Portales públicos abiertos por QR sin autorización.

## Pendientes de precisión que no deben inventarse
- Fuente oficial y alcance exacto del catálogo inicial de residuos de la institución piloto.
- Roles finales y permisos de aprobación por cada transición de lote; propuesta provisional detallada arriba.
- Reglas específicas de correcciones de lotes cerrados y formato definitivo de comprobantes.

Si estos puntos bloquean una implementación segura, conservar la opción restrictiva y registrar el pendiente; no ampliar permisos ni asumir reglas peligrosas.

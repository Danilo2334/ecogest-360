> Actualización 2026-11-16: Q1–Q3 aprobadas por el usuario. Se autorizaron planificación y
> solo fase A. Las propuestas originales siguientes se conservan como antecedente; plan.md,
> tasks.md y contracts/api.md describen la planificación vigente. Monto y credenciales IA
> siguen pendientes y no se habilitó ningún servicio externo.

# Decisiones, compatibilidad y secuencia propuesta V2

Estado: propuestas para revisión; no es plan.md aprobado ni tareas ejecutables. Se difiere el
workflow de plan/tareas conforme al apartado 5 del brief: primero aprobar especificación y UX.

## Preguntas bloqueantes para cerrar especificación

| ID | Decisión | Recomendación (no aprobada) | Alternativa y efecto |
| --- | --- | --- | --- |
| Q1 | Historia y comparación | Comparar períodos cerrados consecutivos de igual número de días, mismos filtros/procedencia y mismo corte de consulta, con valores vigentes; explicitar cobertura desconocida y diferente maduración del compostaje | Comparación histórica reconstruida exigiría versionar datos/cortes y mayor alcance; no implementarla silenciosamente |
| Q2 | Escenarios y planes | Escenario efímero, una hipótesis; reducción de no aprovechables o aumento hipotético de acreditación sobre orgánicos aún disponibles; todos consultan/simulan, solo gestor edita planes; base congelada al iniciar | Persistencia de escenarios, combinación de hipótesis o seguimiento por operador requiere ampliar contratos/permisos y aprobación expresa |
| Q3 | Datos externos y presupuesto | IA externa apagada hasta aprobar contexto agregado mínimo, retención y presupuesto; conversación efímera, sin adjuntos/textos privados en contexto, sin herramientas autónomas | Conservar conversaciones o enviar documentos requiere política adicional; uso sin límite de gasto no se propone |

Q3 tiene una parte de diseño y otra de activación: puede aprobarse la política conservadora
ahora y mantener pendiente el monto máximo. Sin monto autorizado no habrá solicitudes de pago.
La ausencia del PDF Brownfield es una limitación documental, no un bloqueo por decisión del usuario.

## Valores propuestos de negocio y límites

Q1: día según America/Bogota; fechas inclusivas, períodos disjuntos y completos. Comparación de
kg usa valores vigentes de ambas cohortes al consultar. No comparar como si fueran la misma
población de residuos: mismo alcance y duración, cohortes distintas identificadas. Las tasas
son descriptivas; las cohortes recientes pueden tener menor tiempo de tratamiento. La UI muestra
esta advertencia y no concluye deterioro causal. Días sin registros no prueban generación cero.
No seleccionar automáticamente solo áreas con datos excluyendo otras del denominador.

Q2: una hipótesis por cálculo para evitar dobles descuentos. E se obtiene por origen de los
orgánicos no consumidos del universo (incluye generación sin asignar y saldo asignado sin
consumir, sin contarlos dos veces). E excluye entregas, entradas a procesos y procedencia
estimada para acreditación. Base siempre actual, no saldo histórico inferido del corte.
Si el usuario elige corte pasado, se permite observar pero no simular saldo actual como pasado.
N es generación no aprovechable del área/cohorte. Reducción simula menor generación futura:
no elimina consumos existentes ni se ofrece como edición de los registros base.
No sumar N y E como masa potencial intercambiable. Meta nunca obliga a cambiar masas reales.

Planes: borrador editable; inicio congela indicador/base/criterios; gestor registra revisiones
con motivo para acción, responsable, fecha o meta. Cambiar universo/base exige nuevo plan
vinculado, no sustitución de historia. Evaluación usa período posterior cerrado no solapado,
misma duración, filtros y procedencia. Si una corrección invalida comparabilidad se muestra
No evaluable, conservando base anterior y motivo. Estado cerrado puede tener resultado no alcanzado.

## Matriz funcional de roles y datos (propuesta Q2)

| Flujo / datos | Administrador | Operador | Gestor | Consultor | Control |
| --- | --- | --- | --- | --- | --- |
| Observatorio / agregados y fuentes autorizadas | Leer | Leer | Leer | Leer | Institución y filtros en servidor |
| Pasaporte / QR / evidencias | Leer | Leer y operar según V1 | Leer y validar según V1 | Leer | Cada acceso autentica y restringe institución |
| Simular / contexto e hipótesis efímera | Calcular | Calcular | Calcular | Calcular | Ninguna escritura operativa |
| Plan / base, meta, seguimiento | Leer | Leer | Crear, editar, evaluar, cancelar | Leer | Auditoría y conflicto de versión |
| Asistente / contexto mínimo autorizado | Consultar | Consultar | Consultar | Consultar | Sin permisos adicionales al rol |
| Institución / usuarios y catálogo | Mantener | No administrar | No administrar | No administrar | Conservar reglas V1 |
| Incidencias | Crear/leer | Crear/leer | Crear/leer | Leer | No resolver alterando masas |

Responsable del plan puede ser miembro activo de la institución; asignarlo no lo convierte en
gestor ni le concede escritura. Gestor documenta seguimiento. Asignación no manda correo ni notificación.
Los datos personales permitidos en UI autenticada no se envían por defecto al proveedor IA.

## Decisiones técnicas propuestas, sin cambios de código

- Conservar React/TypeScript/Vite/CSS Modules, Python 3.12, Django 5.2/DRF y PostgreSQL 16.
- Extraer navegación, contexto de filtros y consultas por página de App.tsx progresivamente;
  conservar /lotes/{uuid} y sesión. No introducir biblioteca de router/gráficos sin justificarla.
- Componentes visuales compartidos y tipos de dominio explícitos; migrar Row/any por bordes,
  no rehacer todos los servicios como requisito del primer incremento.
- Conservar rutas/respuestas V1; agregar consultas V2 bajo contratos separados tras diseño.
  Listas V1 siguen arrays: paginación V2 debe ser nueva interfaz, no cambio silencioso de forma.
- Reutilizar report/selectores de dominio; evitar cálculos distintos de A en observatorio,
  CSV, simulador o asistente. Reparto por origen de ConsumptionSource sigue siendo fuente.
- Pasaporte como proyección de relaciones existentes, no nueva tabla de eventos ficticios.
- Escenarios sin persistencia en esta propuesta. Planes requieren entidades aditivas de plan,
  revisiones y evaluación; su esquema y migraciones se diseñarán y aprobarán después.
- La rama preserva código, no una instantánea de la base. Antes de migraciones futuras se requiere
  respaldo verificable y ensayo en copia; volver de rama no revierte una migración de datos.

## Diseño de integración OpenAI (propuesta)

La documentación oficial muestra SDK Python y Responses API en el
[quickstart](https://developers.openai.com/api/docs/quickstart). Se propone ese adaptador en
backend, con modelo configurable; SDK/modelo/versiones exactos quedan por seleccionar y fijar
tras evaluar compatibilidad, costes y pruebas. No se instaló ni invocó el proveedor.

Flujo: sesión/CSRF → autorización y cuota → contexto determinista institucional → contexto
mínimo con IDs de evidencia efímeros → proveedor → validación de respuesta → UI con fuentes.
El servidor deriva institución/rol; ignora institución arbitraria suministrada por navegador.
No herramientas SQL, filesystem, web, ejecución de código ni mutaciones. Consultas de dominio
son funciones de solo lectura elegidas por la aplicación, no ejecución libre dirigida por el modelo.

Proponer respuesta estructurada con modo, referencias permitidas e interpretación; las cifras
se renderizan desde el contexto del backend. Rechazar referencias desconocidas y afirmaciones
numéricas no enlazables a valores deterministas; ante fallo mostrar datos verificados y aviso.
El esquema no garantiza verdad: la documentación advierte que
[Structured Outputs puede contener errores](https://developers.openai.com/api/docs/guides/structured-outputs).
Esto requiere corpus de evaluación y límites, no prometer que un filtro vuelve infalible al modelo.

Cada solicitud recibe agregados y etiquetas seguras; excluir nombres personales, receptor,
observaciones libres de BD, contenido de adjuntos y credenciales. La pregunta del usuario sí
se envía si se habilita IA: aviso previo y límite de longitud, con rechazo de patrones de secretos;
no prometer detección perfecta. Sesión nueva o cierre borra conversación local; contexto y fuentes
se vuelven a autorizar cada vez. Respuestas se muestran como texto seguro, sin HTML ejecutable.

Proponer `store=false` y no historial persistente de conversaciones en aplicación. Esto no es
una promesa de retención cero del proveedor: revisar controles y elegibilidad de la cuenta en
[Data controls](https://developers.openai.com/api/docs/guides/your-data) antes de activar datos reales.
Logs locales mínimos: ID de solicitud, estado, duración y consumo agregado; sin prompts, respuestas,
clave ni adjuntos. Métricas de gasto separadas de datos ambientales, con retención a definir.

Valores técnicos iniciales para planificar, no autorizaciones de gasto: pregunta ≤2000 caracteres,
contexto ≤6000 tokens, salida ≤1000 tokens (sujeto al modelo seleccionado), timeout total 25 s,
una consulta simultánea por usuario y 5 solicitudes/minuto/usuario. Sin reintento automático
ante resultado incierto. Cuota por institución y reserva atómica del máximo coste antes de llamar;
conciliar con uso reportado y rechazar si falta presupuesto/precio configurado. Añadir presupuesto
diario autorizado y tope de proyecto; no confiar solo en un aviso visual de coste.
No sustituir modelo automáticamente por uno más caro ni incluir llamadas de pago en CI.

## Riesgos y compatibilidad

| Riesgo | Mitigación propuesta | Verificación futura |
| --- | --- | --- |
| Doble conteo o fórmula divergente | Selectores compartidos y reparto por origen | 25/20/8; múltiples lotes, áreas y procesos |
| Falsa tendencia histórica | Q1, contexto vigente y cobertura explícita | Corrección posterior y cohortes con distinta maduración |
| Pasaporte inventa autor/fecha | Evento persistido o «no disponible» | Lote sin tratamiento, mezcla de procesos |
| Pérdida de navegación o sesión | Conservar enlaces UUID, CSRF, roles y logout | Deep link, refresh, atrás y cambio de usuario |
| Cambio rompe clientes V1 | Adiciones separadas, pruebas de contrato previas | Arrays V1, errores y campos actuales |
| Migración rompe reversibilidad | Aditiva y compatible con código anterior; ensayo en copia | Arrancar V1 sobre esquema ampliado y restauración de prueba |
| Datos ajenos llegan a IA | Contexto acotado servidor; sin IDs arbitrarios | Dos instituciones y sesiones alternadas |
| Inyección o respuesta inventada | Sin herramientas mutadoras; referencias permitidas; validación | Textos maliciosos, cifras falsas, fuente falsa, salida inválida |
| Gasto/latencia descontrolados | Límites y reserva atómica; degradación | Concurrencia, timeout, límite agotado |
| Pantallas vistosas sin flujo | Wireframes con evidencia y acción por rol | Recorrido integrado y pruebas humanas |
| Sobreafirmar evidencia académica | Mantener CHK013/TDD parcial y separar pruebas nuevas | Revisión documental antes de entrega |

## Secuencia para plan y tareas después de aprobación

1. Cerrar Q1–Q3 de diseño; preparar plan.md, research.md, data-model.md, contratos y quickstart
   con las habilidades correspondientes. Presupuesto puede seguir pendiente con IA deshabilitada.
2. Generar tasks.md por historia, pruebas previas a cada cambio y rutas concretas; análisis de
   consistencia requisito→contrato→tarea→prueba. Ninguna tarea ejecutable se aprueba en este documento.
3. Capturar línea base de regresión V1 en base de pruebas dedicada y documentar fallos antes de editar.

| Incremento futuro | Contenido | Puerta de salida |
| --- | --- | --- |
| A / US1 | Tokens/componentes, navegación, contexto y Observatorio | Fórmulas y comparación correctas; flujos V1 accesibles; responsive |
| B / US2 | Lista/detalle y pasaporte autenticado | Cronología exacta, QR anterior válido, saldos idénticos |
| C / US3 | Cálculo efímero y comparación | Límites E/N y cero escrituras de escenarios |
| D / US4 | Planes, auditoría y evaluación | Solo gestor muta; base preservada; evaluación sin éxito ficticio |
| E / US5 | Adaptador, cuotas, contexto y respuesta | Seguridad/fallos con proveedor simulado; prueba real solo con clave/gasto autorizados |
| F | Regresión, accesibilidad y demo | Suites sin regresión; resultados reales documentados y revisión humana separada |

## Casos de verificación propuestos (NO ejecutados)

- V1: suites actuales backend/tests, frontend/tests; Django con PostgreSQL real, Vitest y Playwright.
  No renombrar T008/T014/T019/T026/T032 como completadas por pruebas nuevas.
- US1: 20→25=+25 %, anterior cero, período ausente, intervalos inválidos, suma ranking=universo,
  filtros por institución, CSV consistente, cortes y correcciones vigentes.
- US2: eventos ausentes, un lote en dos procesos, un proceso con dos lotes, evidencia privada,
  UUID anterior, cero autoría/fechas inferidas y cero doble conteo.
- US3: x=0, x=E, x>E, negativo, demasiados decimales, N=0, G'=0, base obsoleta,
  procedencia estimada y comparación de tablas operativas antes/después.
- US4: roles cruzados, responsable ajeno/desactivado, edición concurrente, transiciones inválidas,
  base corregida, período posterior insuficiente, meta no alcanzada y auditoría completa.
- US5: sin clave, timeout, cuota, proveedor no autorizado, inyección en pregunta/textos,
  número/fuente falsa, rechazo del proveedor, respuestas malformadas, otra institución,
  logout durante consulta, filtro cambiado y no exposición de secretos en logs/UI.
- UX: teclado, foco/restauración en panel, lectores de pantalla, gráficos con tabla,
  360/390/768/1280 px, zoom y movimiento reducido. Ejecución humana documentada aparte.

## Bloqueantes y no bloqueantes

Bloqueantes para declarar spec lista: Q1, Q2 y política Q3. Para activar IA: modelo/SDK evaluados,
presupuesto explícito y política de datos compatible con la cuenta. No se pide clave aquí.
No bloqueantes del diseño: copia local del PDF, nombre final de iconos, tipografía local dentro
de la pila propuesta, ejemplos redactados para la demo. No autorizar dependencias nuevas por estética.

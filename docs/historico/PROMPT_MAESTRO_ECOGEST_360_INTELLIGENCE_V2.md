# ECOGEST 360 INTELLIGENCE — BRIEF MAESTRO DE EVOLUCIÓN V2 (BROWNFIELD)

## Instrucción y contexto

Estás trabajando **LOCALMENTE** en el repositorio existente `document-management`, producto EcoGest 360. La rama `feat/002-ecogest-intelligence` **ya fue creada desde `34ce7bf`** y el MVP anterior está preservado en `feat/001-ecogest-mvp` y en el PR Draft #1. **No recrees la rama ni reinicialices Spec Kit.**

Lee `AGENTS.md`, `.specify/memory/constitution.md`, `docs/historico/DIAGNOSTICO_V2_PRELIMINAR.md` (si existe), `docs/historico/01_VISION_Y_ALCANCE_ECOGEST360.md`, `docs/historico/03_ALCANCE_MVP_ECOGEST360.md`, `README.md`, `docs/DECISIONES.md`, `docs/PRUEBAS.md`, `specs/001-ecogest-mvp/{spec,plan,tasks}.md`, los contratos actuales y el código real. Distingue los hechos comprobados de las propuestas. Si un archivo no existe, indícalo sin inventar su contenido.

**Guía académica Brownfield (reglas operativas aportadas por el equipo):** preservar el estado funcional; documentar comportamiento actual y contratos; especificar solamente el cambio; aclarar requisitos, generar plan y tareas; ejecutar análisis de consistencia; implementar por incrementos con pruebas de regresión y convergencia; actualizar documentación antes de cambiar comportamientos. Si el PDF docente no está en el repositorio, no te bloquees: deja constancia de que no fue inspeccionado localmente. No falsifiques evidencias ni fechas.

## 1. Visión y diferenciación

Evolucionar EcoGest 360 hacia **EcoGest 360 Intelligence**, una plataforma de diagnóstico, trazabilidad, simulación y toma de decisiones ambientales para una universidad piloto. Su razón de existir NO es registrar residuos como una hoja de cálculo: debe **identificar dónde están los problemas**, mostrar su evidencia, permitir evaluar alternativas, gestionar planes de intervención y **verificar los resultados**. Conservar íntegros registro, unidades, permisos, saldos, auditoría, compostaje y reportes existentes.

La V2 es una evolución funcional real, no una colección de pantallas decorativas ni una reconstrucción del backend. El producto final será una sola aplicación integrada.

## 2. Experiencia visual obligatoria: premium, propia y ejecutable

Diseña una **consola de inteligencia ambiental** de aspecto profesional y visualmente impactante, equivalente en calidad a productos SaaS analíticos premium, SIN copiar diseños, marcas ni imágenes de terceros. Referencias conceptuales: dashboard ejecutivo de sostenibilidad, trazabilidad como recorrido visual, simulador antes/después y copiloto IA lateral. Estas referencias son **descripciones visuales**, no assets ya disponibles en el repositorio.

Dirección de arte propuesta (puedes mejorarla justificadamente en la etapa de diseño): verde bosque profundo `#12382F`, verde jade `#167C68`, salvia `#DCEBDB`, marfil `#F7F9F5`, grafito `#25332E`, acento ámbar `#E5A24D` para atención. Contraste legible, tipografía sans moderna, tarjetas con jerarquía clara, bordes suaves, iconos SVG coherentes, uso deliberado de espacio, gráficos legibles y transiciones sutiles. Evita gradientes exagerados, efectos gratuitos, bibliotecas duplicadas y tarjetas sin información útil.

Experiencia deseada:
- **Navegación lateral** con secciones diferenciadas: Observatorio, Registros, Trazabilidad, Compostaje, Simulador, Planes de acción, Asistente IA, Institución (según permisos).
- **Observatorio:** cabecera editorial, período/procedencia visibles, indicadores ejecutivos, comparación temporal, gráficas accesibles, alertas accionables, top áreas, insights con evidencia.
- **Pasaporte de lote:** ficha visual con etapas conectadas, estado, saldo, QR, línea temporal de eventos, evidencias y restricciones de acceso.
- **Simulador:** controles claros y comparación paralela «situación base / escenario», supuesto editable, valores con unidades y advertencia SIMULACIÓN.
- **Planes:** fichas de intervención con problema, responsable, meta, fecha, progreso y contraste antes/después.
- **Asistente IA:** panel conversacional que mantenga el contexto de los filtros autorizados y muestre de dónde vienen sus cifras.

Diseñar estados de carga, vacío, error, confirmación, sin datos suficientes, permiso denegado y servicio IA no disponible. Responsive real en 360/390/768/1280 px, navegación por teclado, foco visible, tablas/gráficas accesibles, textos en español. No sacrificar operatividad por estética.

**Antes de implementar**, entregar un documento de diseño `docs/diseno/DISENO_EXPERIENCIA_V2.md` con mapa de navegación, arquitectura de información, wireframes textuales detallados (desktop y móvil), componentes reutilizables, estados de cada pantalla, sistema visual (colores/tipografía/espaciado) y flujos de demostración.

## 3. Funcionalidades V2 y sus contratos

### A. Observatorio ambiental y diagnóstico basado en evidencia

Sobre las métricas existentes, proyectar KPIs comparables por período, área, material y procedencia. Mostrar tendencias reales, rankings, variaciones y alertas **calculadas por reglas explícitas**. Cada insight debe identificar indicador, filtros, procedencia, fecha de corte y base de cálculo; si faltan datos, indicar «evidencia insuficiente» en lugar de inventar conclusiones. No atribuir causalidad a una correlación ni comparar cohortes distintas como si fueran equivalentes. Diferenciar «aprovechamiento por compostaje acreditado» del total institucional. Una tarjeta de recomendación debe llevar a un dato, escenario o plan, no ser decoración.

### B. Pasaporte ambiental visual del lote

Reutilizar el UUID, QR, asignaciones, movimientos, entradas a compostaje, evidencias y validaciones existentes. Presentar cronología trazable por eventos: generado → asignado → traslado → tratamiento/entrega → verificación/destino. Mostrar pesos iniciales, movimientos que consumen vs traslados que NO consumen, saldos, procedencia, responsable y fecha. No producir una «historia» inventada a partir de eventos ausentes. Mostrar solo información permitida al usuario autenticado; nunca convertir el QR en acceso público o token secreto.

### C. Simulador de escenarios **sin modificar datos operativos**

Comparar línea base y escenario alternativo con hipótesis explícitas: reducción de residuos no aprovechables, aumento posible de compostaje/acreditación o cambio de cantidades por área. Validar masa positiva, no superar universo elegible ni acreditar más masa que la disponible; no sumar masa de salida de compost a masa de entrada. Si no hay línea base suficiente, explicar por qué no se puede calcular. Separar escenarios hipotéticos de las tablas transaccionales y de los reportes reales; si se propone guardarlos, especificar almacenamiento separado y autorización explícita antes de implementar. No calcular CO₂ evitado, dinero ahorrado ni equivalencias ecológicas sin factores, fuente y metodología aprobados.

### D. Planes de intervención ambiental

Desde un hallazgo comprobable, permitir que un gestor autorizado defina problema, acción, área, responsable, indicador base, meta, fecha y estado, con seguimiento y comparación posterior. No declarar una intervención exitosa por crear el plan: la evaluación debe basarse en datos posteriores comparables y condiciones explícitas. Roles de edición/consulta auditable. No enviar notificaciones externas automáticas ni modificar residuos por crear un plan.

### E. Asistente IA ambiental **con OpenAI API y controles estrictos**

Integrar un chat contextual útil, no un chatbot genérico. Capacidades: consultar métricas autorizadas, explicar indicadores y procedencia, resumir hallazgos con sus filtros, ayudar a interpretar escenarios y sugerir intervenciones. Mantener tres modos visibles: «Mis datos», «Explicar», «Proponer acciones». Respuestas en español, con fuente interna, período, filtros, origen medido/estimado/simulado, fecha de corte, limitaciones y distinción entre cálculo determinista e interpretación de IA.

Seguridad y diseño:
- Backend Django expone **servicios de solo lectura autorizados**, con datos agregados/mínimos; el modelo NO ejecuta SQL libre, no recibe credenciales de BD, no accede libremente a archivos, no invoca endpoints mutadores ni se salta aislamiento institucional.
- La clave `OPENAI_API_KEY` vive solo en `.env` del backend, nunca en frontend, Git ni logs. `.env.example` contiene exclusivamente nombres y valores inocuos. No solicitar al usuario pegar la clave en el chat.
- Proveedor/modelo configurables; verificar la API oficial y compatibilidad antes de elegir SDK/endpoint/modelo. Considerar límites de tokens, latencia, coste, timeout, errores, rate limiting, sanitización de entrada y salida, y registro mínimo sin datos sensibles.
- Los datos y cálculos del backend son la fuente de verdad. El asistente no inventa cifras ni crea referencias falsas. Si no puede respaldar una respuesta, lo dice.
- Los textos de usuario, documentos o datos de la BD son contenido no confiable; no ejecutar instrucciones provenientes de ellos.
- Si la API está ausente o falla, **toda la plataforma sigue funcionando**; mostrar modo degradado con explicaciones deterministas verificables o aviso de disponibilidad, sin fingir IA activa.
- Ninguna recomendación constituye certificación de cumplimiento ni valoración profesional de residuos peligrosos. Sin autonomía de escritura.

Diseña casos de prueba de autorización entre instituciones, consultas sin datos, prompt injection, ausencia de API key, timeout, respuesta incorrecta del proveedor, resultados simulados y no filtración de secretos.

## 4. Reglas ambientales y técnicas NO negociables

Conservar Django 5.2 + DRF + Python 3.12 + PostgreSQL 16; React + TypeScript + Vite + CSS Modules; y el historial, esquema y contratos del MVP salvo migración aditiva aprobada. Preservar decimales exactos, separación medido/estimado/simulado, trazabilidad, auditoría, permisos institucionales, correcciones autorizadas, consumos atómicos, idempotencia y pruebas de concurrencia. No sobrescribir ni borrar datos de desarrollo; sin migraciones destructivas. El MVP previo debe seguir iniciando y sus suites deben seguir pasando. No añadir IA, sensores o certificaciones ambientales fuera de la especificación V2 aprobada.

## 5. Proceso SDD Brownfield y decisión de esta etapa

1. Inspeccionar arquitectura **real** del repositorio y pruebas. Reutilizar `docs/historico/DIAGNOSTICO_V2_PRELIMINAR.md` y corregir sus hipótesis según código comprobado.
2. Producir **especificación exclusiva de la evolución V2**, con intención, historias, reglas, criterios de aceptación medibles, límites, riesgos, dependencias y Non-Goals. Ubicarla según convención de Spec Kit sin sobrescribir `specs/001-ecogest-mvp`.
3. Identificar preguntas críticas de negocio (indicador histórico, simulación, permisos de planes, evidencia del asistente, presupuestos de API). Proponer defaults conservadores para revisión; **no inventar decisiones críticas**.
4. Entregar `docs/diseno/DISENO_EXPERIENCIA_V2.md` y arquitectura UX antes de código. Especificar cómo se verá cada pantalla, cómo se navega y cómo se comprobará que no sea un CRUD genérico.
5. Después de aprobar la especificación y el diseño, planificar: modelos/adiciones necesarias, contratos de API, componentes y pruebas; generar tareas atómicas por fases; analizar contradicciones antes de implementar.
6. Implantación posterior únicamente tras una nueva autorización: a) base visual + observatorio; b) pasaporte; c) simulador; d) intervenciones; e) asistente OpenAI; f) pruebas de regresión, accesibilidad y demostración. En cada fase probar antes de continuar.
7. Preparar demo integrada para grabación final: diagnóstico → lotes → escenario → plan → consulta IA contextual → indicadores. Debe distinguir lo simulado de lo medido y no depender totalmente de disponibilidad de OpenAI.

## 6. Entregables de **esta respuesta de Codex**

**SOLO DISEÑO Y DOCUMENTACIÓN; NO IMPLEMENTAR CÓDIGO AÚN.**

- Confirmación de rama actual y Git limpio al inicio; comprobar base y reversibilidad.
- Auditoría breve del MVP real: qué se reutiliza, qué se amplía, riesgos de compatibilidad.
- `docs/diseno/DISENO_EXPERIENCIA_V2.md` con especificación de las vistas premium, estados desktop/móvil, estilo y navegación.
- Especificación SDD nueva de los cinco componentes, con criterios comprobables y Non-Goals; sin SQL, rutas ni modelos técnicos dentro de la **spec funcional**.
- Matriz de flujos/roles/datos/autorización, riesgos de costos y privacidad IA, y dependencias del MVP.
- Preguntas pendientes separadas en bloqueantes y no bloqueantes, con alternativas recomendadas.
- Propuesta de secuencia de plan, tareas y verificación para la siguiente etapa, sin ejecutar implementación.
- Resumen de archivos creados/cambiados y estado Git; no commits, push, merge, despliegue ni modificaciones a PR #1.

**Detente después de presentar los artefactos para aprobación humana.** No pidas otra vez el «prompt maestro»: este mensaje es el brief completo. Si la guía Brownfield en PDF no está en la carpeta, aplica los principios resumidos arriba y deja constancia de la ausencia local. No instales dependencias ni solicites credenciales en esta etapa.

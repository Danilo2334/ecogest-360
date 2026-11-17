# EcoGest 360 Intelligence — diagnóstico preliminar Brownfield

Estado: diagnóstico de diseño actualizado tras lectura completa del brief maestro; no es auditoría exhaustiva ni prueba de ejecución.
Fuente recibida: docs/historico/PROMPT_MAESTRO_ECOGEST_360_INTELLIGENCE_V2.md.
La guía académica Brownfield mencionada no se ha identificado en los documentos consultados.

## Base preservada

- Rama de evolución: `feat/002-ecogest-intelligence`, creada desde `34ce7bf24463a3ce476cdb52e9c002f2ab777faf`.
- MVP recuperable en `feat/001-ecogest-mvp`, mismo commit; main permanece en `58bab1f`.
- Constitución 1.1.0 sin cambios; ninguna modificación remota, de aplicación o base de datos.
- Las 38 pruebas corresponden a la ejecución documentada anterior, no se repitieron en esta revisión.
- CHK013 y cinco tareas TDD históricamente parciales conservan su estado.

## Arquitectura observada y reutilización

| Componente | Evidencia | Reutilización y precauciones |
| --- | --- | --- |
| Interfaz React/TypeScript/Vite | frontend/src/app/App.tsx | Navegación por estado, sesión y carga de datos centralizadas; proponer rutas estables y separar consultas por pantalla sin romper sesión ni enlaces de lote |
| Estilos CSS Modules | frontend/src/app/App.module.css y global.css | Evolucionar tokens, jerarquía y componentes accesibles dentro del stack autorizado |
| Formularios y tablas | frontend/src/components/ActionForm.tsx y shared.tsx | Reutilizar errores, estados de carga e idempotencia; formularios específicos para flujos complejos |
| Transporte REST | frontend/src/services/api.ts | Mantener CSRF y sesión; sustituir progresivamente Row/any por contratos tipados |
| Identidad y permisos | backend/organizations/models.py y core/permissions.py | Conservar institución y cuatro roles; nuevos permisos por acción deben especificarse |
| Registros y trazabilidad | backend/waste/, traceability/ | Reutilizar Generation, Lot, Allocation, Movement y ConsumptionSource; no duplicar contabilidad |
| Compostaje | backend/compost/ | Conservar entradas, salida independiente, evidencia y validación |
| Indicadores | backend/reports/selectors.py | Reutilizar filtros por cohorte y procedencia; no presentar corte como reconstrucción histórica completa |
| Persistencia | backend/config/settings.py, compose.yaml | PostgreSQL y ORM existentes; futuras migraciones aditivas y verificadas antes de ejecutarse |

No se ha encontrado integración OpenAI entre las dependencias actuales examinadas. No se instaló ningún SDK.
El panel actual acredita compostaje, no todo el aprovechamiento institucional. Los listados no tienen
paginación según la conciliación técnica del MVP. No hay medición nueva de rendimiento.

## Dirección visual inicial para discusión, no aprobada

Mantener identidad ambiental: verde profundo como color principal, fondo marfil, superficies blancas,
acento ámbar reservado para atención, conforme al brief. Usar tipografía sans-serif legible y números tabulares; evitar
cargar nuevas fuentes externas como condición para funcionar. Proponer escala de espaciado de 4/8 px,
jerarquía clara de títulos y etiquetas, foco visible y estados distinguibles sin depender del color.

Separar navegación de operación (registros, lotes, compostaje, incidencias) de análisis y decisión.
El Observatorio sería la entrada analítica; el detalle de cada lote enlazaría su Pasaporte.
Simulador, Planes y Asistente tendrían destinos identificables y contexto institucional visible.
Los filtros de procedencia, período y área deben permanecer explícitos, también en exportaciones.
En móvil, navegación compacta y formularios de una columna; en escritorio, contenido con ancho
controlado y detalles por selección, evitando una lista interminable de formularios abiertos.

Componentes propuestos: cabecera contextual, filtros persistentes, indicadores con fórmula/fuente,
tabla con detalle, cronología de trazabilidad y estados vacío/carga/error. No mostrar métricas ni
predicciones ficticias para rellenar el diseño. Validar contraste y navegación por teclado con el diseño final.

## Módulos y decisiones trasladadas a la especificación V2

| Módulo solicitado | Base disponible | Decisión de alcance pendiente |
| --- | --- | --- |
| Observatorio | Panel, filtros, distribución y CSV | Series temporales, comparaciones y métricas exactas; reglas para cohortes y ausencia de datos |
| Pasaporte Ambiental | Identificador, QR, movimientos y origen de lote | Unidad del pasaporte, campos, exportación y audiencia; no presumir acceso público ni certificación |
| Simulador | Reglas de masas y separación de procedencias | Variables, fórmulas, supuestos y persistencia; resultados hipotéticos nunca alterarán registros operativos |
| Planes de Intervención | Roles, áreas e incidencias | Responsables, metas, estados, evidencia de seguimiento y permisos de aprobación |
| Asistente IA | Backend autenticado y reportes acotados | Preguntas admitidas, contexto permitido, conservación de conversaciones y presupuesto |

## Restricciones técnicas confirmadas para la IA

Integración opcional exclusivamente mediante backend y adaptador de proveedor; credencial en variable
de entorno, nunca en navegador, Git, QR ni logs. No solicitar ni configurar claves en esta etapa.
El backend debe seleccionar contexto autorizado por institución/rol antes de llamar al proveedor.
Minimizar datos enviados y excluir credenciales, documentos privados y datos personales por defecto.
El asistente no dispondrá de operaciones para cambiar masas, cerrar lotes o validar resultados.
Los cálculos de indicadores seguirán siendo deterministas; las respuestas deben distinguir datos,
supuestos y sugerencias y señalar falta de evidencia. Sin clave o ante fallo, conservar flujo manual.

Modelo, API, límites, retención, costes y SDK quedan para investigación documental oficial al definir
el alcance. Este documento no afirma compatibilidad de una versión específica ni autoriza gasto.

## Secuencia propuesta de diseño y regresión

1. Brief maestro leído; guía Brownfield aplicada por transcripción del equipo, PDF no inspeccionado.
2. Crear spec.md V2 con historias, reglas, aceptación, Non-Goals y permisos por módulo.
3. Validar compatibilidad constitucional sin alterar la constitución; señalar cualquier conflicto.
4. Preparar plan, investigación, modelo de datos, contratos, guía de validación y tareas trazables.
5. Presentar propuesta visual y funcional completa para aprobación antes de programar.
6. Solo tras aprobación: implementar incrementos con regresiones sobre sesión/CSRF, aislamiento,
   masas, concurrencia, idempotencia, QR privado, evidencia y fórmulas de cohortes.
7. Añadir pruebas V2 de separación de simulaciones, permisos de planes, respuestas IA sin evidencia,
   fallo del proveedor y resistencia a instrucciones maliciosas dentro de datos consultados.

La especificación Draft está en specs/002-ecogest-intelligence/spec.md y su diseño en
docs/diseno/DISENO_EXPERIENCIA_V2.md. Se actualizó únicamente el selector .specify/feature.json a la nueva
carpeta. Q1–Q3 requieren revisión; plan y tareas detalladas esperan aprobación conforme al brief.

## Hallazgos ampliados de código y compatibilidad

- core/idempotency.py ejecuta transaction.atomic y pg_advisory_xact_lock antes del recibo;
  core/validation.py restringe por institución y usa select_for_update al solicitar bloqueo.
  Conservar llamada desde las operaciones REST; no asumir que cada servicio es transaccional solo.
- traceability/services.py consume por Allocation/ConsumptionSource, con origen ordenado y
  saldo verificado. No crear una segunda contabilidad para pasaporte o simulador.
- compost/services.py distingue finalizado de confirmado; evidencia confirmada inmutable,
  salida independiente, estimado no acreditable. Serializadores actuales no exponen toda la
  información temporal/autoral de cada entidad; el pasaporte requerirá una proyección adicional
  de campos realmente existentes. Ausencias deben mostrarse, no inferirse como hechos.
- reports/selectors.py usa generación vigente, fecha de confirmación al corte y relaciones
  por origen. No reconstruye cambios históricos ni permite inferir cobertura completa del registro.
- App.tsx mantiene filtros en memoria y ruta especial /lotes/UUID; navegación nueva debe preservar
  ese enlace, evitar contexto cruzado al cerrar sesión y separar cargas por módulo.
- Dependencias Python fijadas; package.json contiene rangos/latest, con package-lock.json para
  reproducir npm ci. No actualizar dependencias masivamente al hacer el rediseño.
- Pruebas existentes incluyen test_vertical, test_security, test_concurrency, test_compost,
  test_compost_provenance, test_audit, test_reports, test_report_performance, test_persistence;
  frontend conserva tests de formularios/fechas y tres recorridos e2e. Se inspeccionaron rutas
  y casos; no se ejecutaron suites en esta fase documental.

Al inicio de este turno la rama era V2 con dos documentos no rastreados: este diagnóstico y
el brief añadido por el usuario. No se describe ese inicio como working tree clean. La rama
se creó en el turno anterior desde un árbol limpio del MVP. Base: 34ce7bf; main: 58bab1f.
La rama preserva código; no es respaldo de base de datos. El PR #1 no fue modificado.

No existe contradicción crítica con la constitución si IA sigue opcional y sin escritura,
se conservan CSS Modules/SVG accesible y no se amplía la acreditación ambiental. El alcance V2
sigue pendiente de aprobación; los Non-Goals V1 no se borraron ni se reinterpretaron como entrega V2.

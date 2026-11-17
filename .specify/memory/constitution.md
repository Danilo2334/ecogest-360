# Constitución del Proyecto: EcoGest 360

> **Estado:** RATIFICADA — versión 1.1.0, aprobada por el usuario el 2026-11-15.
> **Documento base:** docs/plantillas/plantilla_constitucion_sdd.md entregada por la profesora.
> **Propósito:** esta constitución establece reglas transversales del proyecto. Las funcionalidades concretas, flujos, historias y criterios de aceptación se desarrollarán después en las especificaciones (`spec.md`).

## 1. Naturaleza del Proyecto

**EcoGest 360** es una aplicación web de **gestión ambiental y economía circular**, inicialmente diseñada para una institución universitaria piloto y preparada para soportar otras organizaciones en futuras fases. Está dirigida a administradores institucionales, gestores ambientales, operadores de recolección y usuarios académicos autorizados.

Su propósito central es **registrar y caracterizar los residuos sólidos, preservar la trazabilidad de su recolección y destino, dar seguimiento al aprovechamiento —incluido el compostaje de orgánicos— y producir indicadores e informes verificables** que apoyen decisiones ambientales.

Integra tres enfoques complementarios en un solo producto: gestión ambiental (EcoGest), trazabilidad por lotes/QR (concepto de TraceFood) y aprovechamiento orgánico (concepto de AgroPilot). No pretende administrar integralmente los cultivos ni reemplazar la evaluación profesional del cumplimiento ambiental.

El MVP operará para una única institución universitaria piloto. La administración de múltiples instituciones y su gestión pública quedan para fases futuras; el aislamiento de datos sigue siendo obligatorio.

## 2. Stack Tecnológico (Reglas de Implementación)

- **Frontend / UI:** React con TypeScript y Vite; estilos responsivos con CSS Modules como solución inicial; futuras ampliaciones requieren justificación y aprobación. Priorizar accesibilidad, claridad, rendimiento y componentes reutilizables. Para los gráficos del MVP se permite SVG nativo accesible, con alternativa textual o tabular, sin biblioteca adicional. Si se aprueba una biblioteca de gráficos en una fase posterior, se elegirá y documentará una sola, evitando duplicidades y manteniendo accesibilidad.
- **Backend:** Python 3.12 como versión objetivo, Django 5.2 LTS y Django REST Framework para la API REST. Evitar agregar otros frameworks de servidor salvo aprobación explícita.
- **Base de Datos:** PostgreSQL mediante ORM y migraciones de Django. Usar restricciones e integridad transaccional para movimientos de masas, lotes y estados. Prohibido usar bases de datos o archivos temporales como sustituto de la fuente de verdad en operaciones centrales.
- **Lenguaje:** TypeScript/TSX en frontend, Python en backend y SQL únicamente cuando sea necesario y esté justificado; documentación en español, código con convenciones técnicas estables.
- **Herramientas complementarias permitidas:** generación de QR sin credenciales embebidas; exportación CSV/PDF; pruebas automatizadas para API, permisos y flujos; control de versiones Git. El proveedor de IA será una integración **opcional** aislada tras una interfaz, no una dependencia obligatoria de la operación.
- **Configuración y despliegue:** secretos exclusivamente mediante variables de entorno no versionadas; dependencias fijadas y documentadas; no modificar la instalación global de Python para adaptar el proyecto.

## 3. Reglas de Dominio y Lógica de Negocio

Estas reglas son obligatorias. El agente de IA debe respetarlas estrictamente:

1. **Trazabilidad verificable:** toda generación de residuo debe tener fecha, institución, sede/área, material, cantidad, unidad, origen del dato y responsable. Toda transición posterior debe mantener referencia al origen y registrar quién, cuándo y por qué.
2. **Integridad de cantidades:** no aceptar pesos negativos o nulos como registros de masa; normalizar unidades a kilogramos con aritmética decimal. No autorizar movimientos o asignaciones superiores al saldo disponible del lote. Los movimientos no constituyen nueva generación y jamás deben duplicar masa en los indicadores.
3. **Clasificación ambiental:** distinguir residuos aprovechables, orgánicos aprovechables y no aprovechables de acuerdo con el esquema colombiano aplicable. La separación ordinaria utiliza blanco para aprovechables, verde para orgánicos aprovechables y negro para no aprovechables. Los residuos peligrosos y de manejo especial o diferenciado se identifican por separado; no se clasificarán automáticamente en los contenedores ordinarios.
4. **Aprovechamiento demostrado:** diferenciar los residuos potencialmente aprovechables de los residuos con aprovechamiento efectivamente confirmado mediante un evento y evidencia verificable. Los pendientes se contabilizan aparte.
5. **Compostaje con datos reales:** registrar masa de entrada, controles del proceso y masa de salida como registros independientes. No asumir igualdad entre peso inicial y compost obtenido, ni afirmar que el producto cumple características de calidad sin ensayos correspondientes.
6. **Calidad y procedencia de datos:** marcar cada valor como medido, estimado o simulado; los indicadores e informes deben preservar esta distinción y mostrar fuente, fecha de corte, fórmula y limitaciones.
7. **Acceso y aislamiento:** todos los accesos requieren autenticación excepto contenido público expresamente diseñado para ello. Usuarios con roles institucionales solo pueden operar sobre los registros autorizados de su organización, con controles aplicados en backend y consultas.
8. **Correcciones auditadas:** los registros validados no pueden alterarse o eliminarse de forma silenciosa. Las correcciones requieren motivo, usuario, momento y rastro anterior/posterior.
9. **Seguridad de archivos y QR:** los archivos adjuntos se validan por tamaño, tipo y permisos. El QR no expone secretos ni permite acceso no autorizado; solo identifica un lote o abre una consulta con controles correspondientes.
10. **IA bajo supervisión:** la IA puede sugerir clasificación, explicar procedimientos generales y apoyar análisis, pero **no puede modificar cantidades, cerrar lotes, autorizar destinos, certificar cumplimiento ni alterar datos automáticamente**. Toda clasificación sugerida requiere validación humana.
11. **Indicadores consistentes:** las tasas deben declarar fórmula y período, evitar doble conteo y usar cohortes comparables (por ejemplo, masa aprovechada de los lotes generados en un período dividida por la masa generada de esos mismos lotes, con pendientes y fecha de corte explícitos).
12. **Responsabilidad ambiental:** no emitir recomendaciones para manipular residuos peligrosos sin protocolos revisados; no presentar predicciones de emisiones, compostaje o impactos como mediciones certificadas.

## 4. Estructura y Estilo de Código

- **Estructura:** repositorio organizado al menos en `/frontend`, `/backend` y `/docs`; los archivos de gobierno SDD se preservan en `.specify/` y las habilidades de Codex en `.agents/skills/`; conservar `.github/` si existe. Dentro de backend, separar dominios (identidad/organizaciones, catálogo, registros, trazabilidad, procesos, reportes); dentro de frontend, separar páginas, componentes, servicios API, validaciones y tipos.
- **Estilo:** funciones y componentes pequeños; separación de responsabilidades; validación en servidor además de interfaz; reglas de dominio reutilizables; consultas controladas; transacciones para cambios de saldos; no generar abstracciones que no respondan a requisitos aprobados.
- **Nomenclatura:** Python según PEP 8 (`snake_case` en funciones/variables, `PascalCase` en clases); React/TypeScript con `PascalCase` en componentes, `camelCase` en funciones/variables y tipos definidos explícitamente. APIs, estructuras y nombres de campos consistentes y documentados.
- **Pruebas y documentación:** cada regla crítica tendrá tests automatizados de casos correctos, límites y errores; cambios de modelo deben incluir migraciones y pruebas; documentación de instalación y operación actualizada por fase. No sobrescribir trabajo existente sin inspeccionar impacto y crear respaldo cuando proceda.

## 5. Manejo de Errores y Validaciones

- **UI:** mensajes comprensibles en español para campos obligatorios, unidades inválidas, saldos insuficientes, archivos incompatibles, permisos y fallos de red. Mantener los datos del formulario cuando sea seguro; mostrar carga, vacío y errores; no revelar trazas, tokens, rutas internas o información de otras organizaciones.
- **Backend:** validar entradas y permisos antes de mutar información; utilizar códigos HTTP adecuados (400 por entrada inválida, 401 sin autenticación, 403 sin autorización, 404 recurso inexistente o no visible, 409 conflicto de estado/saldo). Responder con formato de error consistente; proteger integridad con validaciones transaccionales y restricciones en base de datos; registrar errores técnicos sin secretos ni archivos sensibles.
- **Integridad y concurrencia:** impedir que dos operaciones simultáneas extraigan el mismo saldo. Las confirmaciones de recolección, entregas y resultados deben ser transaccionales y resistentes a reintentos, con idempotencia en las operaciones que consumen saldo.
- **IA y terceros:** cuando falle la API de IA, conservar el flujo manual y mostrar un mensaje honesto; nunca generar análisis inventados como sustitución silenciosa.

## 6. Comportamiento del Agente de IA (Reglas SDD)

- **Cero Código Sombra (Shadow Code):** implementar únicamente lo definido en especificaciones aprobadas (`spec.md`) y sus tareas; no añadir funcionalidades, dependencias ni complejidad «por si acaso». Prohibido adelantar otras fases sin autorización.
- **Fuente de la Verdad:** si una solicitud contradice la constitución o aparece inconsistencia entre documentos, **detener la implementación**, describir el conflicto y solicitar revisión del documento correspondiente antes de modificar el código.
- **Trabajo supervisado y por etapas:** primero elaborar y aprobar constitución, después especificación funcional, plan técnico, tareas e implementación. Presentar cambios por bloque y facilitar revisión humana antes de avanzar al siguiente.
- **Transparencia:** diferenciar hechos verificados, supuestos y pendientes; no afirmar que se realizaron pruebas sin ejecutarlas; entregar comandos de reproducción, pruebas realizadas, resultados y limitaciones.
- **Seguridad y preservación:** no revelar ni versionar claves, no eliminar archivos o registros existentes sin permiso, no ejecutar migraciones destructivas sin aprobación, no instalar servicios externos sin justificar dependencia.
- **Exactitud ambiental:** usar fuentes identificables para reglas normativas y mantener la distinción entre sugerencia de IA y dato de campo. No inventar mediciones, tasas, cumplimiento legal o resultados.
- **Definición de terminado:** una funcionalidad solo está lista cuando cumple los criterios de aceptación aprobados, tiene validaciones y permisos, pruebas ejecutadas, documentación y demostración funcional.

---

### Gobernanza, aprobación y revisión

La versión 1.0.0 es la primera constitución ratificada, aprobada el 2026-11-15.
La enmienda 1.1.0, ratificada por aprobación explícita del usuario el 2026-11-15,
permite SVG nativo en §2; conserva las demás reglas y los seis apartados docentes.
El usuario autorizó iniciar `speckit-specify`; la planificación y la implementación requieren revisión posterior de las especificaciones.
Las enmiendas documentarán motivo, reglas afectadas e impacto en especificaciones, plan,
tareas y pruebas. El usuario aprobará los cambios antes de implementarlos.
El versionado será MAJOR para cambios incompatibles, MINOR para nuevas reglas compatibles
y PATCH para aclaraciones. Toda revisión o PR comprobará conformidad con esta constitución.
Las decisiones y pruebas se registrarán en `docs/DECISIONES.md` y `docs/PRUEBAS.md`.

La visión no autoriza funciones futuras. El alcance inicial procede de
`docs/historico/03_ALCANCE_MVP_ECOGEST360.md`; los permisos por transición y criterios de aceptación
se definirán en `spec.md`, sin endpoints ni SQL. IA, campañas, metas, IoT, comercio,
gestión agrícola, certificaciones y despliegue público multiinstitución quedan fuera del MVP.
PDF es una mejora posterior al flujo prioritario y CSV.

Las pruebas cubrirán autenticación, permisos y aislamiento, masas positivas, saldos insuficientes,
concurrencia y reintentos, doble conteo, persistencia, compostaje y dashboard.
README, ejemplos de entorno sin secretos y migraciones permitirán reproducir el arranque.
No declarar pruebas ejecutadas sin evidencia.

La demo etiquetará también las salidas de compost como simuladas. Los resultados reales
requieren pesaje independiente. No sumar entrada y salida como aprovechamientos distintos
del mismo residuo. La especificación precisará evidencia de aprovechamiento y denominador cero.

No fabricar autorías, revisiones ni fechas. Las cuentas reales son `Danilo2334` y
`francisco3788`; cada participante verificará las contribuciones atribuidas.
Antes de un push se comprobarán cuenta activa e identidad Git. Push, merge, despliegue
público, gastos y cambios destructivos requieren autorización explícita para esa acción.

**Versión**: 1.1.0 | **Ratificación**: 2026-11-15
**Última modificación**: 2026-11-15

## Lista de verificación antes de aprobarla

- [x] El propósito y los usuarios del proyecto están claros.
- [x] El stack tecnológico está definido conforme a las decisiones del usuario.
- [x] Las reglas críticas de negocio son verificables.
- [x] La estructura y las convenciones de código están especificadas.
- [x] Se describe cómo validar datos y manejar errores.
- [x] El agente de IA tiene límites claros y no puede ampliar el alcance sin autorización.
- [x] Se eliminaron los textos de instrucción y los marcadores pendientes del documento final.

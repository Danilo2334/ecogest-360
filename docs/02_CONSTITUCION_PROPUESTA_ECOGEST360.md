# Constitución del Proyecto: EcoGest 360

> **Estado:** BORRADOR PARA REVISIÓN ACADÉMICA Y APROBACIÓN DEL EQUIPO.  
> **Documento base:** plantilla_constitucion_sdd.md entregada por la profesora.  
> **Propósito:** esta constitución establece reglas transversales del proyecto. Las funcionalidades concretas, flujos, historias y criterios de aceptación se desarrollarán después en las especificaciones (`spec.md`).

## 1. Naturaleza del Proyecto

**EcoGest 360** es una aplicación web de **gestión ambiental y economía circular**, inicialmente diseñada para una institución universitaria piloto y preparada para soportar otras organizaciones en futuras fases. Está dirigida a administradores institucionales, gestores ambientales, operadores de recolección y usuarios académicos autorizados.

Su propósito central es **registrar y caracterizar los residuos sólidos, preservar la trazabilidad de su recolección y destino, dar seguimiento al aprovechamiento —incluido el compostaje de orgánicos— y producir indicadores e informes verificables** que apoyen decisiones ambientales.

Integra tres enfoques complementarios en un solo producto: gestión ambiental (EcoGest), trazabilidad por lotes/QR (concepto de TraceFood) y aprovechamiento orgánico (concepto de AgroPilot). No pretende administrar integralmente los cultivos ni reemplazar la evaluación profesional del cumplimiento ambiental.

## 2. Stack Tecnológico (Reglas de Implementación)

- **Frontend / UI:** React con TypeScript y Vite; estilos responsivos con una solución CSS de uso consistente. Priorizar accesibilidad, claridad, rendimiento y componentes reutilizables. Elegir y documentar una sola biblioteca de gráficos para evitar duplicidades.
- **Backend:** Python 3.12 o 3.13, Django 5.2 LTS y Django REST Framework para la API REST. Evitar agregar otros frameworks de servidor salvo aprobación explícita.
- **Base de Datos:** PostgreSQL mediante ORM y migraciones de Django. Usar restricciones e integridad transaccional para movimientos de masas, lotes y estados. Prohibido usar bases de datos o archivos temporales como sustituto de la fuente de verdad en operaciones centrales.
- **Lenguaje:** TypeScript/TSX en frontend, Python en backend y SQL únicamente cuando sea necesario y esté justificado; documentación en español, código con convenciones técnicas estables.
- **Herramientas complementarias permitidas:** generación de QR sin credenciales embebidas; exportación CSV/PDF; pruebas automatizadas para API, permisos y flujos; control de versiones Git. El proveedor de IA será una integración **opcional** aislada tras una interfaz, no una dependencia obligatoria de la operación.
- **Configuración y despliegue:** secretos exclusivamente mediante variables de entorno no versionadas; dependencias fijadas y documentadas; no modificar la instalación global de Python para adaptar el proyecto.

## 3. Reglas de Dominio y Lógica de Negocio

Estas reglas son obligatorias. El agente de IA debe respetarlas estrictamente:

1. **Trazabilidad verificable:** toda generación de residuo debe tener fecha, institución, sede/área, material, cantidad, unidad, origen del dato y responsable. Toda transición posterior debe mantener referencia al origen y registrar quién, cuándo y por qué.
2. **Integridad de cantidades:** no aceptar pesos negativos o nulos como registros de masa; normalizar unidades a kilogramos con aritmética decimal. No autorizar movimientos o asignaciones superiores al saldo disponible del lote. Los movimientos no constituyen nueva generación y jamás deben duplicar masa en los indicadores.
3. **Clasificación ambiental:** distinguir residuos aprovechables, orgánicos aprovechables y no aprovechables de acuerdo con el esquema colombiano aplicable. Los residuos peligrosos y de manejo especial o diferenciado tendrán reglas y advertencias independientes; no se clasificarán automáticamente en los contenedores ordinarios.
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

- **Estructura:** repositorio organizado al menos en `/frontend`, `/backend` y `/docs`; los archivos de gobierno SDD se preservan en `.specify/` y las instrucciones de agente en `.github/`. Dentro de backend, separar dominios (identidad/organizaciones, catálogo, registros, trazabilidad, procesos, reportes); dentro de frontend, separar páginas, componentes, servicios API, validaciones y tipos.
- **Estilo:** funciones y componentes pequeños; separación de responsabilidades; validación en servidor además de interfaz; reglas de dominio reutilizables; consultas controladas; transacciones para cambios de saldos; no generar abstracciones que no respondan a requisitos aprobados.
- **Nomenclatura:** Python según PEP 8 (`snake_case` en funciones/variables, `PascalCase` en clases); React/TypeScript con `PascalCase` en componentes, `camelCase` en funciones/variables y tipos definidos explícitamente. APIs, estructuras y nombres de campos consistentes y documentados.
- **Pruebas y documentación:** cada regla crítica tendrá tests automatizados de casos correctos, límites y errores; cambios de modelo deben incluir migraciones y pruebas; documentación de instalación y operación actualizada por fase. No sobrescribir trabajo existente sin inspeccionar impacto y crear respaldo cuando proceda.

## 5. Manejo de Errores y Validaciones

- **UI:** mensajes comprensibles en español para campos obligatorios, unidades inválidas, saldos insuficientes, archivos incompatibles, permisos y fallos de red. Mantener los datos del formulario cuando sea seguro; mostrar carga, vacío y errores; no revelar trazas, tokens, rutas internas o información de otras organizaciones.
- **Backend:** validar entradas y permisos antes de mutar información; utilizar códigos HTTP adecuados (400 por entrada inválida, 401 sin autenticación, 403 sin autorización, 404 recurso inexistente o no visible, 409 conflicto de estado/saldo). Responder con formato de error consistente; proteger integridad con validaciones transaccionales y restricciones en base de datos; registrar errores técnicos sin secretos ni archivos sensibles.
- **Integridad y concurrencia:** impedir que dos operaciones simultáneas extraigan el mismo saldo. Las confirmaciones de recolección, entregas y resultados deben ser transaccionales o idempotentes según su función.
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

## Lista de verificación antes de aprobarla

- [x] El propósito y los usuarios del proyecto están claros.
- [x] El stack tecnológico propuesto está definido y requiere visto bueno del equipo/profesora.
- [x] Las reglas críticas de negocio son verificables.
- [x] La estructura y las convenciones de código están especificadas.
- [x] Se describe cómo validar datos y manejar errores.
- [x] El agente de IA tiene límites claros y no puede ampliar el alcance sin autorización.
- [x] Se eliminaron instrucciones de apoyo y marcadores de campos pendientes.

**Pendiente para convertirla en constitución definitiva:** revisión del estudiante, revisión de requisitos de la profesora y validación de las tecnologías propuestas. Una vez aprobada, ejecutar `/speckit.constitution` en Copilot Chat para generar o actualizar `.specify/memory/constitution.md`. Este archivo de `docs/` es material de trabajo y NO sustituye automáticamente la constitución de Spec Kit.

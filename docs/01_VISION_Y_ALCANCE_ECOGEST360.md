# EcoGest 360 — Visión, alcance y diseño funcional

> Estado: **propuesta inicial para revisión**. No es una especificación aprobada ni autoriza implementar código.  
> Proyecto: **EcoGest 360 — Plataforma inteligente de gestión ambiental y economía circular**.  
> Escenario piloto: **una universidad**. Arquitectura preparada para incorporar otras instituciones y organizaciones después.

## 1. Problema y propósito

Las instituciones generan residuos sólidos, pero con frecuencia carecen de un registro integrado que permita responder cuánto se genera, dónde, qué tipo de material se produce, quién lo recoge, qué destino tiene y qué parte se aprovecha efectivamente. Esto dificulta caracterizaciones, seguimiento de acciones e informes sustentados en evidencias.

**Propósito:** construir una plataforma web para registrar, caracterizar, rastrear y analizar el manejo de residuos sólidos, con especial interés en el aprovechamiento de orgánicos mediante compostaje y el seguimiento del destino de materiales. Debe servir a la vez como producto de ingeniería de software y como herramienta metodológica para un trabajo universitario de ingeniería ambiental.

## 2. Fusión conceptual (una sola aplicación)

- **EcoGest:** catálogo de residuos, clasificación, generación, recolección, indicadores, metas y reportes.
- **TraceFood (concepto de trazabilidad, no la aplicación agrícola completa):** identificación por lote, movimientos, responsables, evidencias y códigos QR.
- **AgroPilot (concepto de ciclo orgánico, no el sistema agronómico completo):** seguimiento del compostaje y del destino del compost para uso agrícola.

**Cadena diferencial:** lugar de generación → registro de peso/tipo → lote identificable/QR → recolección → recepción → tratamiento o entrega → resultado verificado → indicadores e informe.

El producto **no** incluye por ahora la gestión integral de cultivos, ventas de alimentos, logística de cosechas ni certificación jurídica de cumplimiento ambiental.

## 3. Personas y permisos

- **Administrador institucional:** crea sedes/áreas, incorpora miembros, configura catálogos autorizados, revisa reportes.
- **Gestor ambiental:** valida registros, revisa resultados, crea metas, consulta indicadores, genera informes.
- **Operador de registro y recolección:** registra pesajes, lotes, movimientos y evidencias de su institución.
- **Consultor académico:** consulta datos y reportes autorizados, sin poder alterar información.
- **Administrador de plataforma:** rol técnico restringido para mantenimiento; no se confunde con los otros roles.

La autorización se comprueba SIEMPRE en el servidor. Ningún usuario puede consultar registros de otra organización solo cambiando una URL o un identificador.

## 4. Módulos funcionales

### M1. Instituciones, sedes, áreas y usuarios
Registro de una institución piloto, sedes y espacios generadores (cafeterías, aulas, oficinas, laboratorios). Roles con permisos diferenciados y trazabilidad de cambios. El esquema de datos admite más de una organización sin exponer información entre ellas.

### M2. Catálogo y clasificación ambiental
Materiales y subcategorías; separación en fuente de residuos ordinarios conforme a reglas colombianas: blanco para aprovechables, verde para orgánicos aprovechables, negro para no aprovechables. **Los peligrosos y de manejo especial o diferenciado** se identifican aparte, requieren procedimientos de gestión distintos y no se asignan automáticamente a estos tres contenedores.

### M3. Registro y caracterización de residuos
Fecha/hora, sede, área, material, categoría, cantidad con unidad normalizada a kg, origen del dato (medido/estimado/simulado), método de medición, responsable y evidencia opcional. Registros revisables y rectificables con auditoría.

### M4. Lotes, recolección y trazabilidad (inspirado en TraceFood)
Crear un lote desde cantidades disponibles, identificador público aleatorio y QR; registrar eventos de recolección, transporte, recepción, entrega a gestores y cierre; evidenciar quién hizo qué y cuándo. Las transferencias parciales deben respetar el saldo del lote; no se puede usar la misma masa dos veces.

### M5. Compostaje y aprovechamiento orgánico (inspirado en AgroPilot)
Seleccionar entradas orgánicas elegibles y registrar un proceso de compostaje; registrar fecha de inicio, observaciones y mediciones manuales opcionales (temperatura, humedad, etc.) con unidad y fecha; registrar salidas como compost obtenido mediante **peso medido independientemente**; registrar destino o uso declarado. No se infiere equivalencia 1:1 entre masa entrante y compost final, ni se emiten certificaciones sobre calidad agronómica sin análisis técnicos.

### M6. Analítica y tablero de control
Kilogramos registrados por institución/sede/área, distribución por categorías, evolución temporal, cantidad entregada, cantidad **efectivamente** aprovechada con evidencia, cantidad pendiente de destino, metas y comparaciones entre períodos. Mostrar procedencia y fecha del dato; permitir filtrar únicamente registros medidos, sin mezclar simulaciones.

### M7. Informes y evidencia académica
Reportes por período y ámbito, metodología de captura, registros trazables, tablas, gráficos, tasas cuya fórmula esté explícita y exportación a CSV/PDF. Los informes deben señalar datos faltantes, pendientes, simulados y límites metodológicos.

### M8. Asistente ambiental con IA (expansión controlada)
Ayuda a identificar materiales mediante descripción o fotografía y a interpretar tendencias, usando reglas y fuentes revisadas. Toda clasificación propuesta por IA requiere confirmación humana; registrar versión/modelo cuando aplique y no confundir una predicción con una medición. El registro, la trazabilidad y los indicadores deben funcionar aunque la API de IA no esté disponible. No enviar datos sensibles a servicios externos sin autorización.

### M9. Campañas, metas y educación (expansión)
Crear campañas de sensibilización, objetivos, actividades y seguimiento; comparar periodos con aclaración de variables y evidencia, evitando atribuir causalidad sin un diseño de evaluación adecuado.

## 5. Ejemplo de caso de uso central

1. El operador de la cafetería registra **25 kg medidos de residuos orgánicos**.
2. El gestor valida tipo, área y cantidad; se crea lote QR.
3. Un operador registra 20 kg transferidos a compostaje y 5 kg con otro destino autorizado: el sistema conserva saldo y no duplica masas.
4. Se documenta el ingreso de 20 kg al proceso, con mediciones periódicas registradas como datos, no generadas automáticamente.
5. Al finalizar se registra **el peso real** de compost obtenido y su destino. La diferencia de masa de un proceso biológico no se considera por sí sola error o pérdida injustificada.
6. El dashboard distingue **generado**, **recogido**, **en proceso**, **entregado**, **aprovechado confirmado** y **pendiente** sin sumar la misma masa como nuevo residuo.
7. Se genera reporte del período para apoyar el análisis de ingeniería ambiental.

## 6. Reglas de negocio esenciales

1. No permitir cantidades negativas o cero en registros de masa; exigir unidad y convertir a kg con precisión decimal.
2. No permitir asignaciones, retiros o movimientos que superen el saldo disponible del lote.
3. No contar recolecciones, movimientos o entradas a procesos como nueva generación de residuos.
4. No considerar un material "aprovechado" hasta que exista un resultado o entrega confirmada y registrada según el criterio definido.
5. Marcar claramente cada valor como **medido**, **estimado** o **simulado** y no mezclar estos grupos en indicadores científicos sin filtro y nota metodológica.
6. Proteger el ámbito de cada organización y aplicar autorizaciones en todas las rutas y consultas.
7. Conservar bitácora de rectificaciones: usuario, fecha, campo afectado y motivo. Evitar eliminación física de registros ambientales validados.
8. No permitir que la IA altere pesos, clasificaciones finales, estados o decisiones ambientales sin confirmación y permisos.
9. El QR solo identifica el lote y abre una vista con autorización; no contiene secretos ni expone datos privados.
10. La separación blanco/verde/negro se aplica al ámbito correspondiente; residuos de gestión diferenciada se tratan con reglas particulares.
11. Los resultados del compostaje se registran como mediciones propias. No exigir igualdad entre masa de entrada y masa de compost resultante.
12. La trazabilidad debe relacionar cada resultado con registros de origen y movimientos verificables.

## 7. Modelo de datos conceptual (orientativo, no definitivo)

- Institucion, Sede, Area, Usuario, Membresia/Rol
- TipoResiduo, Material, CategoriaGestion
- RegistroGeneracion, Evidencia, EventoAuditoria
- LoteResiduo, MovimientoLote, Recoleccion, Entrega, GestorDestino
- ProcesoCompostaje, EntradaProceso, MedicionProceso, ResultadoProceso
- MetaAmbiental, Campania (posteriores)
- ConsultaIA, RevisionClasificacionIA (posteriores; sin secretos ni datos personales innecesarios)

Definir cardinalidades, borrados, restricciones de unicidad e índices durante la planificación técnica, no inventarlos en la constitución.

## 8. Indicadores sugeridos y precauciones

- **Generación del período (kg):** suma de registros válidos de generación, filtrados por ámbito y por condición de medición.
- **Distribución por material:** peso de cada categoría / peso total de generación para el mismo ámbito y período.
- **Aprovechamiento verificado (kg):** sumatoria de resultados confirmados evitando el doble conteo por movimientos intermedios.
- **Tasa de aprovechamiento:** se define rigurosamente por **cohorte de generación y período de seguimiento**: kg de esa cohorte finalmente aprovechados / kg de esa misma cohorte generados × 100. Si hay material pendiente, informar la tasa como provisional, con fecha de corte. No usar flujos de cohortes diferentes en numerador y denominador.
- **Pendientes de destino (kg):** masa cuyo destino final no esté acreditado según modelo de seguimiento; no confundir con residuos no aprovechables.
- **Desempeño de metas:** valor logrado frente al objetivo con período y metodología explícitos.

No presentar reducción de emisiones de CO₂, impactos ambientales o calidad del compost como valores medidos a menos que haya metodología y datos suficientes; si se usan factores de emisión, documentar fuente, supuestos, incertidumbre y etiqueta de estimación.

## 9. Tecnología propuesta (pendiente de validación en clase)

- Frontend: React + TypeScript + Vite; interfaz responsiva y accesible; biblioteca visual ligera.
- Backend: Python 3.12 o 3.13 + Django 5.2 LTS + Django REST Framework.
- Base de datos: PostgreSQL, con migraciones gestionadas y ORM de Django.
- Reportes: CSV/PDF; gráficos en frontend.
- QR: código generado a partir de identificador público no secreto.
- IA: integración opcional mediante adaptador sustituible, inicialmente Gemini si está autorizado y configurado.
- Pruebas: backend (unitarias, API, permisos, integración), frontend (componentes y flujos), revisión de migraciones y accesibilidad básica.
- Entorno: configuración por variables de entorno; Docker Compose solo si simplifica las pruebas de todos los integrantes.

**Nota:** se propone Python 3.12/3.13 para minimizar incompatibilidades del ecosistema aun cuando el sistema tenga instalada otra versión. No desinstalar ni modificar el Python global.

## 10. Plan por incrementos SDD

- **Fase 0 — Diseño:** constitución aprobada, glosario ambiental, alcance de piloto, especificaciones verificables y prototipos.
- **Fase 1 — Base sólida:** cuentas/permisos, institución y áreas, catálogo, registros, validaciones, dashboard inicial, pruebas y migraciones.
- **Fase 2 — Trazabilidad:** lotes, saldos, eventos, QR, evidencias, entregas y pruebas de integridad de masa.
- **Fase 3 — Circularidad y valor académico:** compostaje, destinos, indicadores verificados, reportes y exportaciones.
- **Fase 4 — Potenciadores:** asistente con IA bajo revisión humana, campañas, metas y mejoras de experiencia.

Cada fase requiere especificación, plan técnico, tareas, implementación, pruebas y revisión antes de continuar. El agente no implementará fases futuras por anticipado.

## 11. Dos entregables académicos, un mismo sistema

**Curso SDD / agentes:** repositorio, constitución, especificaciones, casos de uso, arquitectura, tablero de tareas, pruebas automatizadas, capturas y demostración funcional.

**Curso ambiental:** problema, área piloto, protocolo de caracterización, fuente y calidad de los datos, registros reales o simulados **claramente identificados**, análisis de indicadores, discusión de límites metodológicos y propuesta de mejora. No presentar datos de ejemplo como mediciones obtenidas en campo.

## 12. Definición mínima de listo por funcionalidad

- Requisito con criterios de aceptación y límites claros.
- Modelo/validaciones autorizados implementados y revisados.
- Permisos y aislamiento de datos probados.
- Tests relevantes pasando y evidencia de ejecución.
- Flujos funcionales en interfaz responsiva.
- Documentación de decisiones y variables de configuración actualizada.
- Sin datos inventados en reportes, sin credenciales en Git y sin modificaciones fuera del alcance aprobado.

## 13. Referencias de base verificadas

- Minambiente (Colombia), preguntas frecuentes, Resolución 2184 de 2019: https://www.minambiente.gov.co/preguntas-frecuentes/
- Minambiente, Guía nacional para separación adecuada de residuos (2022): https://economiacircular.minambiente.gov.co/wp-content/uploads/2022/06/guia-nacional-para-la-adecuada-gestion-de-residuos-colombia-2022.pdf
- Django 5.2, versión de soporte extendido: https://docs.djangoproject.com/en/5.2/releases/5.2/

> Estas referencias son un punto de partida. Antes de implementar un módulo regulado se deben verificar las normas aplicables a la organización, tipo de residuo y actividad.

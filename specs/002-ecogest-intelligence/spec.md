# Feature Specification: EcoGest 360 Intelligence — evolución V2

**Feature Branch**: `feat/002-ecogest-intelligence`
**Created**: 2026-11-15
**Status**: Dirección aprobada el 2026-11-16. Ejecución local A–E e integración autorizada por orden final del usuario; IA sin llamadas pagadas hasta presupuesto y bandera explícita.
**Input**: [Brief maestro](../../docs/PROMPT_MAESTRO_ECOGEST_360_INTELLIGENCE_V2.md).

Esta especificación describe solo la evolución del MVP. Conserva la constitución 1.1.0 y
las reglas de `../001-ecogest-mvp/spec.md`. La exclusión de IA y planes en V1 se mantiene
como alcance histórico de V1; V2 propone incorporarlos sin cambiar las reglas permanentes.
Guía Brownfield aplicada según transcripción del equipo; PDF no inspeccionado localmente.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnosticar con evidencia (Priority: P1)

Como usuario institucional quiero localizar áreas y períodos que requieren atención y
abrir los registros que respaldan el hallazgo para decidir dónde intervenir.
**Why this priority**: Establece el contexto verificable que usarán escenario, plan y asistente.
**Independent Test**: Consultar dos períodos de prueba y contrastar cifras, filtros y hallazgos con sus registros.
**Acceptance Scenarios**:
1. Dados 25 kg generados, 20 kg de entrada acreditada y 8 kg de salida independiente simulada,
   al filtrar esa cohorte se muestran G=25, A=20, pendiente=5 y 80 %, nunca A=28 ni A=8.
2. Dados dos períodos comparables con generación 20 y 25 kg, al comparar se muestran +5 kg y +25 %;
   se identifica cada período, procedencia y fecha de consulta, sin afirmar causalidad.
3. Dado un período sin registros o anterior con cero, no se inventa una tendencia: variación
   porcentual No calculable; se diferencia ausencia de registros de cero sumado en una consulta.
4. Dado un hallazgo de masa pendiente, al abrir su evidencia se conservan filtros y aparecen
   los registros contribuyentes; los vínculos a simular o crear plan respetan el rol.

### User Story 2 - Consultar el pasaporte de un lote (Priority: P1)

Como usuario autorizado quiero reconstruir el recorrido documentado de un lote para conocer
origen, saldo, responsables y evidencia sin confundir traslado con consumo o cierre con verificación.
**Why this priority**: Reutiliza trazabilidad y hace verificable el diagnóstico.
**Independent Test**: Abrir un lote con eventos conocidos y uno sin tratamiento; consultar también sin sesión.
**Acceptance Scenarios**:
1. Un traslado de 20 kg en un lote de 25 muestra efecto sobre saldo de 0; entrada a compostaje
   de 20 deja saldo 5. Ambos eventos tienen referencia y fecha propias.
2. Un lote sin verificación muestra «Sin verificación registrada»; no se crea un hito cumplido.
3. Un lote repartido entre procesos muestra ramas y masas de entrada por proceso; una salida
   compartida se etiqueta como salida del proceso, sin repartirla al lote como medición propia.
4. El mismo QR sigue identificando el lote y requiere sesión y permisos; referencia ajena no revela datos.

### User Story 3 - Evaluar escenarios sin alterar la operación (Priority: P2)

Como usuario quiero contrastar una línea base con una hipótesis explícita para comprender su
posible efecto antes de proponer una intervención.
**Why this priority**: Permite decidir sin fabricar mediciones ni consumir saldos.
**Independent Test**: Calcular escenarios sobre un conjunto congelado para la consulta y comprobar que
registros, lotes, procesos e indicadores operativos quedan idénticos.
**Acceptance Scenarios**:
1. Dados G=25, A=20 y 5 kg orgánicos elegibles disponibles, una hipótesis de 3 kg adicionales
   muestra A hipotético=23, pendiente hipotético=2 y 92 %, con etiqueta ESCENARIO HIPOTÉTICO.
2. Solicitar 6 kg adicionales supera los 5 elegibles y se rechaza. Una procedencia estimada
   no puede presentar acreditación adicional; permite analizar generación sin acreditar.
3. Una reducción hipotética de 2 kg sobre 10 kg no aprovechables, con G=25 y A=0,
   produce G hipotético=23 y reducción=2; no convierte esos 2 kg en compostaje acreditado.
4. Si cambian datos operativos después de cargar la base, se marca la base desactualizada y
   se exige recalcular antes de trasladar el contexto a un plan.

### User Story 4 - Gestionar intervenciones y contrastar resultados (Priority: P2)

Como gestor quiero convertir un hallazgo en un plan con responsable, meta y seguimiento,
para comprobar después el cambio observado con evidencia comparable.
**Why this priority**: Conecta análisis y acción humana sin automatizar cambios ambientales.
**Independent Test**: Crear plan, registrar seguimiento, evaluar período posterior y comprobar permisos/auditoría.
**Acceptance Scenarios**:
1. Crear un plan requiere problema, acción, área, responsable institucional activo, indicador,
   base con evidencia, meta, fecha objetivo y estado. No modifica residuos ni envía avisos externos.
2. Un consultor o administrador sin rol gestor intenta editar: se rechaza sin cambios.
3. Completar actividades no significa meta alcanzada. Si falta período posterior comparable,
   resultado «No evaluable»; si el valor no cumple la meta, «Meta no alcanzada».
4. Una modificación autorizada de meta o responsable conserva motivo, autor y valores anteriores;
   la base de un plan iniciado no se sobrescribe silenciosamente por correcciones posteriores.

### User Story 5 - Consultar un asistente contextual controlado (Priority: P3)

Como usuario quiero explicar mis indicadores y explorar acciones con asistencia claramente
identificada, conservando fuentes y la decisión humana.
**Why this priority**: Enriquece los otros módulos, que deben funcionar aunque no haya IA disponible.
**Independent Test**: Consultar con contexto conocido, sin datos, con contexto ajeno y con proveedor indisponible.
**Acceptance Scenarios**:
1. En «Mis datos», preguntar por una tasa muestra las cifras verificadas, fórmula, período,
   procedencia, corte y enlace interno a la evidencia usada.
2. En «Explicar», una explicación general se identifica como tal; en «Proponer acciones»,
   las sugerencias no se presentan como resultados logrados ni se guardan automáticamente.
3. Si una respuesta propone una cifra o fuente no respaldada, se retiene la interpretación
   y se presenta un aviso con las cifras verificadas; no se publican referencias falsas.
4. Si falla el servicio, aparece «IA no disponible» y continúa la consulta determinista.
5. Una instrucción maliciosa que pida leer otra institución, revelar secretos o alterar masas
   no obtiene esas capacidades ni modifica información; los textos consultados son datos, no órdenes.

### Edge Cases

- Períodos de distinta duración, filtros distintos, días sin registros y períodos abiertos:
  bloquear comparación automática incompatible y explicar límites de cobertura.
- Línea base con G=0: tasa No calculable. Cero reducción significa escenario sin cambio;
  masas registradas siguen exigiendo valores estrictamente positivos.
- Mezcla de procedencias: mantener vista descriptiva separada; no producir un porcentaje conjunto
  ni enviar una mezcla silenciosa al simulador, plan o asistente.
- Múltiples lotes por proceso: mostrar relación muchos-a-muchos sin duplicar salida o acreditación.
- Evidencia incompleta o eliminada del acceso del usuario: no inventar contenido ni reutilizar permisos antiguos.
- Responsable desactivado: impedir nueva asignación; plan existente muestra necesidad de reasignación,
  preserva responsable anterior y seguimiento.
- Dos gestores editando: detectar conflicto de versión, no sobrescribir el trabajo ajeno.
- Cambio de filtros durante respuesta IA: conservar contexto original en la respuesta; avisar que
  no corresponde al filtro actual y permitir nueva consulta explícita.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Conservar acceso, cuatro roles, contratos de operación, saldos, procedencias, auditoría,
  lotes/QR, compostaje y exportación del MVP, sin pérdida o conversión automática de datos.
- **FR-002**: Ofrecer navegación integrada Observatorio, Registros, Trazabilidad, Compostaje,
  Simulador, Planes de acción, Asistente IA e Institución según permisos; mantener acceso a Incidencias.
- **FR-003**: Toda pantalla analítica muestra institución, área/material, período, procedencia y
  fecha de corte; conservar el contexto al navegar y permitir limpiarlo explícitamente.
- **FR-004**: Observatorio presenta G, A de compostaje, pendiente, tasa y distribución; A solo
  entradas acreditadas del universo consultado, salida de compost independiente.
- **FR-005**: Comparar períodos solo con reglas y límites visibles. Q1 aprobada: períodos completos equivalentes sobre datos vigentes, sin reconstrucción histórica y con cobertura explícita..
- **FR-006**: Variación absoluta = actual − anterior; porcentual = (actual − anterior)/anterior ×100
  solo con anterior positivo; tasas se comparan en puntos porcentuales, no como masa.
- **FR-007**: Ordenar áreas por masa generada o pendiente seleccionada, en orden descendente,
  desempate por nombre e identificador; mostrar hasta cinco y permitir ver todas las contribuyentes.
- **FR-008**: Hallazgos deterministas: pendientes >0, generación creciente en períodos comparables
  y falta de datos de comparación. Cada hallazgo indica regla, cifras, fuentes y acción pertinente;
  no se califica riesgo ambiental por un umbral arbitrario ni se atribuye causalidad.
- **FR-009**: El pasaporte muestra identificador y QR existentes, origen, material, procedencia,
  masa asignada, saldo y cronología con fechas/responsables disponibles. Dato ausente se declara ausente.
- **FR-010**: Distinguir eventos logísticos, consumos, finalización y verificación; la representación
  de ramas no suma dos veces masas ni inventa fechas, autores o rendimientos por lote.
- **FR-011**: Solo un usuario autorizado consulta pasaporte y evidencia; mostrar QR no concede acceso público.
- **FR-012**: El simulador usa base identificable, hipótesis explícitas y unidades; separa el escenario
  de registros operativos. Recalcular o descartar no crea movimientos ni acreditación real.
- **FR-013**: Propuesta de simulación conservadora: una hipótesis por ejecución, reducción de no
  aprovechables o aumento de acreditación hipotética sobre orgánicos disponibles elegibles. Cada una
  puede acotarse por área. La variación libre de cualquier masa queda fuera de esta primera V2.
- **FR-014**: Para aumento hipotético: 0≤x≤E, A'=A+x, G'=G y A'≤G'; E es masa orgánica aún disponible
  de la misma cohorte/procedencia, sin entregas ni entradas ya consumidas. No asumir rendimiento de salida. El saldo elegible es actual; un corte histórico no habilita simulación de disponibilidad pasada.
- **FR-015**: Para reducción: 0≤r≤N, G'=G−r y A'=A; N es generación no aprovechable de la base.
  Rechazar inconsistencias A'>G'. G'=0 permite solo A'=0 y tasa No calculable. Resultado hipotético
  no es un registro de masa cero. No persistir escenarios en esta propuesta.
- **FR-016**: Planes y elegibilidad del simulador se rigen por Q2. Q2 aprobada: simulación efímera de una hipótesis y planes persistentes editables solo por gestor, sin escritura ambiental..
- **FR-017**: Cada plan conserva problema, acción, área, responsable, indicador/unidad, período y valor
  base, meta con dirección, fecha objetivo, estado y evidencia de seguimiento; todos de una institución.
- **FR-018**: Estados propuestos: borrador → en curso → en evaluación → cerrado; cancelar requiere motivo.
  Cerrar exige evaluación explícita (alcanzada/no alcanzada/no evaluable), no exige resultado favorable.
  Registrar avances no cambia las métricas ambientales. Sin borrado de historial.
- **FR-019**: Evaluar el mismo indicador, área/material y procedencia en períodos completos de igual
  duración y separados; conservar valor base al iniciar y mostrar si su fuente fue corregida.
  Una comparación no prueba causalidad ni certifica éxito ambiental. Los planes simulados se identifican.
- **FR-020**: Toda edición/seguimiento/transición de plan identifica autor, momento y motivo; detectar
  edición concurrente. Propuesta: solo gestor edita, demás roles consultan; responsable no recibe permisos nuevos.
- **FR-021**: Asistente ofrece «Mis datos», «Explicar» y «Proponer acciones», con contexto visible y
  respuestas en español, separando evidencia determinista, interpretación y sugerencia.
- **FR-022**: Cifras y referencias proceden de fuentes internas autorizadas; la interpretación solo puede
  referirse a esas fuentes. Sin evidencia suficiente debe decirlo, no adivinar.
- **FR-023**: Asistente no cambia datos, no ejecuta instrucciones dentro de textos consultados, no
  certifica cumplimiento ni da instrucciones operativas de manejo peligroso sin protocolos revisados.
- **FR-024**: Ausencia, error o demora del servicio conserva toda función no IA y muestra degradación
  explícita. No sustituir silenciosamente IA por texto fingido ni reintentar sin límites.
- **FR-025**: El uso externo requiere política aprobada de contexto mínimo, retención y presupuesto.
  Q3 aprobada: contexto agregado mínimo, conversación efímera e IA apagada hasta autorizar presupuesto y credenciales..
- **FR-026**: Mostrar carga, vacío, error recuperable, confirmación, falta de evidencia y permiso denegado;
  conservar entradas seguras ante error y prevenir doble envío de operaciones existentes.
- **FR-027**: Soportar 360/390/768/1280 px, teclado, foco visible, etiquetas, alternativas tabulares de
  gráficos y movimiento reducido; ningún significado depende solo del color.
- **FR-028**: No publicar información privada, secretos o adjuntos en respuestas, exportaciones de contexto
  o registros técnicos; aplicar permisos de nuevo a cada consulta, incluso tras cambio de sesión.

### Key Entities *(include if feature involves data)*

- Contexto de análisis: institución, filtros, procedencia, períodos, corte, cobertura y limitaciones.
- Hallazgo: regla cumplida, valores y referencias; es una lectura derivada, no una medición nueva.
- Pasaporte: representación de un lote y sus relaciones existentes, sin nueva identidad ambiental.
- Escenario: base temporal e hipótesis efímera; nunca transacción de residuos.
- Plan de intervención: decisión humana, base, meta, responsable, estado y evaluación.
- Seguimiento: observación/evidencia y autor de una actividad, separada del indicador ambiental.
- Respuesta asistida: contexto, cifras verificadas, fuentes, interpretación y estado de disponibilidad.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100 % de escenarios de regresión V1 conserva sus masas, permisos y resultados;
  historial TDD parcial y CHK013 no se declaran completados por construir V2 (FR-001).
- **SC-002**: Cada KPI y hallazgo de las pruebas tiene fórmula, filtros, procedencia, corte y evidencia;
  20→25 produce +25 %, ausencia de base nunca un crecimiento inventado (FR-003–008).
- **SC-003**: El pasaporte representa todos y solo los eventos de los lotes de prueba, con saldo
  idéntico al registro operativo; cero accesos ajenos exitosos (FR-009–011).
- **SC-004**: Los escenarios de US3 coinciden con cálculo independiente; cero modificaciones
  operativas antes/después y cero acreditaciones sobre procedencia estimada (FR-012–016).
- **SC-005**: Todos los cambios de planes probados conservan auditoría; ningún plan se declara
  meta alcanzada sin comparación válida y ningún rol no gestor escribe (FR-017–020, sujeto Q2).
- **SC-006**: En el corpus de seguridad, todas las cifras y fuentes mostradas en respuestas tienen
  respaldo autorizado; proveedor inválido, sin clave y timeout muestran degradación, con cero
  filtraciones o escrituras en esos casos. No equivale a garantía universal de exactitud IA (FR-021–025,028).
- **SC-007**: Un participante recorre diagnóstico → pasaporte → escenario → plan → consulta contextual
  con guion escrito en ≤20 minutos, registrando ayuda y dificultades; no hay scroll horizontal
  de página en los cuatro anchos y el recorrido es realizable por teclado (FR-002,026–027).
- **SC-008**: Una consulta analítica responde en ≤2 s en al menos 95 de 100 muestras con 10 000
  generaciones y 10 usuarios concurrentes en entorno documentado; IA muestra espera y salida
  controlada en ≤30 s. Son objetivos propuestos, no resultados obtenidos (FR-004,024).

## Assumptions

- Una universidad piloto, usuarios y catálogo actuales; no hay nueva administración multiinstitución.
- Q1–Q3 aprobadas por el usuario el 2026-11-16; presupuesto/modelo de IA pendientes de activación, no de fase A.
- Datos vigentes pueden reflejar correcciones: se informa ese límite en toda comparación.
- No se da por hecho que falta de registro signifique ausencia de residuos.
- La red externa solo es necesaria para IA; el servicio se configura después de aprobación.
- El archivo maestro contiene reglas Brownfield suministradas por el equipo; no se afirma lectura del PDF.

## Non-Goals

- Cambiar la constitución, reescribir el backend, sustituir stack o ampliar acreditación a entregas externas.
- Persistir o compartir escenarios, combinar múltiples hipótesis o reconstruir toda la historia de correcciones.
- Datos ficticios presentados como reales, atribución causal automática, certificaciones, dinero/CO₂/equivalencias sin metodología. Se admite la cohorte simulada explícita FR-029.
- Notificaciones externas, SQL libre, agentes con escritura, navegación libre o lectura de adjuntos por IA.
- Portal público QR, cámaras/IoT, aplicaciones nativas, pagos, despliegue o migraciones destructivas.
- Dar por completadas revisión de PR, CHK013 o evidencia TDD histórica.

## Clarifications — 2026-11-16

Aprobación explícita recibida en el adjunto del usuario: solo implementar fase A tras análisis.
Observatorio usa por defecto los últimos 30 días completos (hasta ayer Bogotá) y Medido.
Comparación automática con los 30 días precedentes; usuario puede cambiar intervalo. Intervalo
máximo para serie diaria: 366 días. Si falta un extremo o abarca hoy, mostrar comparación no
disponible; no inventar un intervalo. Misma procedencia, área, material y corte para ambas cohortes.
La tasa usa datos vigentes al corte y advierte maduración desigual. En «Todas», mostrar desglose
por procedencia y no tasa combinada; exportación conserva el comportamiento V1 explícitamente.
Serie omite línea continua a través de días sin registros; estos se identifican en tabla.
Fase A no ofrece acciones funcionales de módulos futuros; hallazgos llevan a registros filtrados.

## Refinamiento A aprobado — 2026-11-16

- **FR-029**: Cohorte demostrativa opcional, identificada SIMULADO, en una institución separada: 28 fechas, tres áreas y tres materiales; dos períodos consecutivos de 14 días. Su creación explícita es atómica, repetible sin duplicación ni modificación de datos anteriores. Documentar y probar antes de ejecutar. Nunca sembrar al iniciar la aplicación.
- **FR-030**: Visualizar G = A + (G − A), sin sumar salidas de compost ni movimientos; mostrar distribución por material y evolución con huecos honestos. Los KPI permiten consultar la cohorte base conservando filtros, sin afirmar que todos sus registros están acreditados.
- **FR-031**: Cada hallazgo comunica observación, magnitud, límite interpretativo, recomendación humana y acceso a la cohorte de evidencia; el área destacada conserva los otros filtros al explorar.
- **FR-032**: Fechas explicativas en español de Colombia, controles nativos accesibles, lectura de hallazgos próxima a KPI en móvil y detalles secundarios desplegables.
- **SC-009**: Repetir la generación mantiene IDs y cantidades; colisión de usuarios o institución aborta sin cambios. Todas las nuevas masas son simuladas. La cohorte produce una comparación calculable, 14 puntos diarios y tres áreas; balance y distribución concilian con la generación, tanto sin filtros como por área/material.
- **SC-010**: Capturas reales antes/después a 360/390/768/1280, sin desbordamiento; recorridos de teclado y filtros conservados comprobados. Regresión backend/frontend y build aprobados. CHK013 sigue pendiente.

Antecedente: este refinamiento se detuvo para revisión. La orden final posterior autoriza B–E, commits locales y migraciones aditivas; no publicación ni gasto real.

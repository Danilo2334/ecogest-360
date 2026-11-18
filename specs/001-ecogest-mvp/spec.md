# Feature Specification: EcoGest 360 — MVP ambiental universitario

**Feature Branch**: `feat/001-ecogest-mvp`; rama base: `main`. Al redactar la especificación aún no se había creado la rama de implementación.

**Created**: 2026-11-15

**Status**: Aprobado para implementación el 2026-11-15, incluidos A1 y A2.

**Input**: MVP integrado de gestión ambiental, trazabilidad y compostaje para una universidad.
Fuentes: constitución ratificada 1.0.0, visión del producto, alcance MVP y plantilla funcional docente.
Las prioridades siguientes ordenan el trabajo; las cinco áreas forman parte de esta entrega.

## Clarifications

### Session 2026-11-15

- Q: ¿Quién confirma operaciones ordinarias y resultados? → A: Q1 B; operador confirma operaciones ordinarias autorizadas, gestor valida aprovechamiento final, con permisos, saldo y estados comprobados.
- Q: ¿Se corrigen masas consumidas o lotes cerrados? → A: Q2 A; se bloquean, se auditan las correcciones permitidas previas y los errores históricos se registran como incidencias pendientes sin cambiar el historial.
- Q: ¿Qué masa y evidencia acreditan compostaje? → A: Q3 A; entradas por lote de procesos finalizados y validados por gestor, con salida independiente, fecha, responsable y evidencia verificable de destino, sin doble conteo.

### Reglas operativas y casos derivados

- Cierre de CHK004 aprobado por el usuario: solo un proceso de entradas medidas, con salida
  medida independientemente y evidencia verificable de tratamiento/destino, puede acreditar
  aprovechamiento real. Los procesos estimados no se confirman ni aportan A en el MVP, aunque
  tengan salida y evidencia; su regularización queda fuera de alcance. Los simulados completan
  exclusivamente la demostración y conservan su procedencia en cantidades, evidencia e indicadores.
  Una validación nunca convierte estimado o simulado en medido.

- Matriz de permisos: administrador mantiene cuentas, roles, espacios y catálogo; operador
  registra y confirma generación, lotes, movimientos, entradas, mediciones, salida y cierre;
  gestor consulta, valida resultados y corrige generación no asignada; consultor solo consulta.
  Todos pueden consultar lo autorizado y registrar una incidencia salvo el consultor, que solo consulta.
  El administrador no hereda permisos ambientales. No se permite autoasignar un rol superior.
- Generación confirmada está disponible inmediatamente. El formulario no confirmado no es
  generación persistida. El gestor puede validar su clasificación; esa revisión no crea masa.
- Lote abierto tiene saldo positivo; agotado tiene saldo cero; cierre explícito del operador
  exige saldo cero y ausencia de procesos vinculados abiertos. El cierre no acredita destino.
- Proceso en curso acepta entradas y controles; una salida independiente y destino declarado
  permiten finalizarlo. Finalizado bloquea cambios en entradas y salida; gestor confirma solo
  con evidencia completa. Un rechazo conserva pendiente con motivo y permite aportar evidencia
  adicional, sin editar masas. Resultado confirmado es inmutable en el MVP.
- Corrección permitida: gestor corrige fecha, material, área, procedencia o masa de generación
  sin asignaciones, con motivo y valores antes/después. No editar identificadores, institución
  o responsable original. Las correcciones se reflejan en el reporte vigente y quedan auditadas.
- Una incidencia contiene referencia, motivo, fecha y autor; queda pendiente de tratamiento,
  visible al gestor, sin alterar saldo, estado ni aprovechamiento. No hay resolución automática.
- Evidencia de destino contiene documento privado o referencia verificable, receptor, fecha,
  descripción y autor. El gestor registra cuándo verificó, qué revisó y su decisión con motivo.
  Una referencia textual sin elementos verificables no basta. En demostración todo comprobante
  y salida es simulado, y cualquier confirmación es solo del universo simulado.
- La fecha de generación selecciona la cohorte; la fecha de confirmación limita A al corte.
  Los reportes usan valores vigentes corregidos y explican que no reconstruyen versiones pasadas
  de generación. El corte no es una instantánea histórica de todas las correcciones.
- «Pendiente de acreditación» = G − A para masa de origen, e incluye saldo, en proceso y entregas
  sin prueba final. Esas categorías son vistas de la misma masa, no sumandos de generación.
- Casos Q1: operador confirma entrada y reduce saldo inmediatamente; gestor sin rol operador
  no confirma movimientos; operador no valida resultados finales; consultor no escribe incidencias.
- Casos Q2: corregir 25 a 24 kg sin lote deja 24 kg y auditoría; con asignación se rechaza y mantiene
  25 kg; ante lote cerrado se registra incidencia sin cambiar masa ni historial.
- Casos Q3: proceso con 20 kg simulados de entrada y 8 kg simulados de salida, sin comprobante,
  aporta A=0; tras validación completa aporta A=20, nunca 28 ni 8. Con G=25 la tasa es 80 %
  y pendiente=5. Revalidar no duplica A. Un corte anterior a validación conserva A=0.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acceder con permisos institucionales (Priority: P1)

Como administrador quiero organizar usuarios, espacios y materiales de la universidad para
que cada persona consulte o registre únicamente lo autorizado.

**Why this priority**: Protege la información y establece el contexto del registro.

**Independent Test**: Con usuarios y espacios de prueba identificados como tales, comprobar
acceso y prohibiciones de cada rol sin depender de registros ambientales reales.

**Acceptance Scenarios**:

1. Dado un administrador autenticado, cuando incorpora un usuario y asigna un rol institucional,
   entonces ese usuario obtiene solo las capacidades del rol asignado.
2. Dado un consultor, cuando intenta crear o modificar cualquier registro, entonces se rechaza
   la operación y los datos permanecen iguales.
3. Dada una sesión cerrada o un identificador de otra organización, cuando se consulta información,
   entonces no se revelan registros ni evidencias. Esto incluye consultas mediante QR y reportes.
4. Dado un material peligroso o especial, cuando se configura el catálogo, entonces no puede
   aparecer como material ordinario blanco, verde o negro.

### User Story 2 - Registrar generación y caracterización (Priority: P1)

Como operador quiero registrar y recuperar pesajes con su procedencia para conocer la generación.

**Why this priority**: Es el origen verificable de todas las cantidades posteriores.

**Independent Test**: Registrar un pesaje simulado y recuperarlo tras cerrar y abrir sesión.

**Acceptance Scenarios**:

1. Dados fecha, área, material, responsable y 25 kg simulados, cuando se guarda el registro,
   entonces se recuperan esos valores y su etiqueta de simulación sin modificaciones.
2. Dado un peso cero, negativo, no numérico o sin unidad, cuando se intenta registrar,
   entonces se explica el error y no se crea generación ni lote.
3. Dados registros medidos, estimados y simulados, cuando se filtra por área, período,
   material y procedencia, entonces solo se muestran los que cumplen todos los filtros.
4. Dado un registro validado, cuando se intenta editar o borrar directamente, entonces se
   rechaza; cualquier corrección autorizada conserva valores anteriores y motivo.

### User Story 3 - Seguir lotes sin duplicar masa (Priority: P1)

Como operador quiero identificar lotes y seguir sus movimientos para conocer saldo y destino.

**Why this priority**: Impide que una misma masa se asigne o entregue varias veces.

**Independent Test**: Partir de generación simulada disponible y verificar asignación y movimientos.

**Acceptance Scenarios**:

1. Dados 25 kg disponibles, cuando se crea un lote de 25 kg, entonces queda asociado al origen
   y no es posible crear un segundo lote usando nuevamente esos mismos 25 kg.
2. Dado ese lote, cuando se confirma la asignación de 20 kg a compostaje, entonces el saldo
   disponible es 5 kg; una solicitud posterior de 6 kg se rechaza sin alterar el historial.
3. Dada una operación confirmada, cuando se reenvía la misma operación, entonces se conserva
   un único efecto y un único descuento; si cambia su contenido se informa conflicto.
4. Dado un saldo de 5 kg y dos consumos simultáneos de 4 kg, entonces como máximo uno se
   confirma, queda 1 kg y el otro se rechaza sin descuento parcial.
5. Dado un QR, cuando un usuario autorizado lo consulta, entonces ve el lote y sus eventos;
   el mismo QR no permite acceso a usuarios sin permisos.
6. Dado un lote cerrado, cuando se solicita un movimiento ordinario, entonces se rechaza.

### User Story 4 - Documentar compostaje y resultados (Priority: P2)

Como operador quiero vincular entradas orgánicas y resultados independientes para seguir el proceso.

**Why this priority**: Hace trazable el aprovechamiento sin inventar rendimiento.

**Independent Test**: Con un lote orgánico simulado, crear proceso y registrar una salida simulada
independiente; confirmar su evidencia solo mediante la validación del gestor descrita en FR-019.

**Acceptance Scenarios**:

1. Dados 20 kg orgánicos disponibles, cuando se confirma su entrada en un proceso,
   entonces se vinculan origen, responsable y fecha y se consumen una sola vez.
2. Dado material no orgánico o saldo insuficiente, cuando se intenta incorporarlo,
   entonces se rechaza sin cambiar proceso ni saldos.
3. Dado un proceso con entrada de 20 kg simulados, cuando se registra una salida de prueba
   de 8 kg simulados, entonces se conservan ambas cantidades independientes; no se crean
   8 kg adicionales de generación ni se muestran esos valores como mediciones de campo.
4. Dado un resultado sin evidencia aceptada, entonces figura pendiente y no aumenta el
   aprovechamiento verificado. El cierre operativo por sí solo no constituye verificación.
5. Dada una medición opcional de proceso, cuando se registra, entonces conserva valor,
   unidad, fecha y responsable; nunca se genera una medición automáticamente.

### User Story 5 - Consultar indicadores y exportar (Priority: P2)

Como gestor o consultor quiero consultar cifras filtradas y su metodología para elaborar informes honestos.

**Why this priority**: Permite analizar lo registrado con límites y procedencia visibles.

**Independent Test**: Usar un conjunto de prueba conocido con varias procedencias y comparar
manualmente totales del panel y CSV bajo los mismos filtros y corte.

**Acceptance Scenarios**:

1. Dados 25 kg de generación simulada y un traslado de 20 kg, cuando se consulta generación,
   entonces el total sigue siendo 25 kg, nunca 45 kg.
2. Dados datos mixtos, cuando se selecciona solo medidos, entonces ni simulados ni estimados
   contribuyen a filas, gráficos, numeradores, denominadores o exportación.
3. Dado un universo sin generación válida, entonces la tasa muestra «No calculable» con
   denominador cero; no presenta un porcentaje artificial ni un error técnico.
4. Dados filtros y corte iguales, cuando se exporta CSV, entonces contiene el mismo conjunto
   autorizado y permite reproducir los totales; textos con comas, comillas y saltos se conservan.
5. Dado un material potencialmente aprovechable sin confirmación, entonces aparece como
   pendiente, sin sumarse al aprovechamiento verificado.

### Edge Cases

- Una operación fallida no deja descuentos, entradas ni eventos de confirmación parciales.
- Un traslado logístico del mismo material no constituye generación ni consumo final adicional.
- Las correcciones no pueden producir saldos negativos ni romper relaciones ya confirmadas.
- La consulta de un QR inexistente no revela información de otros lotes.
- Un período sin datos se distingue de un fallo de consulta; ambos se explican en español.
- Las salidas de compost no se igualan automáticamente a las entradas ni se usan para
  calcular pérdidas ambientales o calidad agronómica sin metodología.
- Una evidencia inaccesible o inválida no permite acreditar aprovechamiento.
- Cerrar sesión revoca el acceso de esa sesión; los errores no revelan datos privados.

## Requirements *(mandatory)*

### Functional Requirements

Los requisitos se organizan a continuación según las cinco áreas docentes. Las decisiones Q1–Q3 se incorporan en la sección Clarifications. Los permisos y estados siguientes delimitan el MVP.

## Features principales

### 1. Gestión institucional, usuarios, roles y clasificación ambiental

- **FR-001**: Permitir inicio y cierre de sesión de usuarios autorizados, sin inscripción pública.
- **FR-002**: El administrador administra usuarios, roles, espacios y catálogo de la universidad
  piloto. No se ofrece administración de otras instituciones en esta versión.
- **FR-003**: Aplicar mínimo privilegio a toda consulta, modificación, evidencia, QR y exportación.
  El consultor solo consulta; el operador captura registros y eventos; el gestor valida información.
  El rol administrador no recibe automáticamente permisos de validación ambiental.
- **FR-004**: Permitir consultar y mantener materiales ordinarios diferenciando aprovechables,
  orgánicos aprovechables y no aprovechables. **Peligrosos y especiales no son ordinarios**.
  Las categorías usadas históricamente conservan su identificación, aunque dejen de ofrecerse.
- **FR-005**: Resolver responsables y momento de validación de generación, asignaciones,
  movimientos, entradas, resultados y cierres antes de habilitar sus transiciones.
  Decisión Q1 aprobada: el operador confirma registros, creación de lotes, movimientos, entradas, finalización operativa y cierres ordinarios; el gestor valida exclusivamente resultados de aprovechamiento. Cada confirmación ordinaria afecta el saldo en el mismo acto, sin cola de aprobación ni reserva pendiente.

### 2. Registro y caracterización de residuos

- **FR-006**: Registrar fecha, sede/área, material, cantidad en kg, responsable y procedencia
  `medido`, `estimado` o `simulado`; registrar método de medición o estimación cuando corresponda.
- **FR-007**: **Aceptar únicamente masas positivas, expresadas con precisión decimal y unidad**;
  rechazar datos inválidos sin alterar registros previos.
- **FR-008**: Listar, filtrar y recuperar detalles e historial. Conservar información al volver a
  iniciar sesión. No crear valores ambientales para rellenar una pantalla vacía.
- **FR-009**: Conservar auditoría de correcciones: usuario, fecha, motivo, valor anterior y nuevo.
  No permitir borrado silencioso de información validada ni modificar su procedencia sin historial.
  Decisión Q2 aprobada: no modificar masas ya consumidas ni lotes cerrados. El gestor puede corregir generación solo mientras no tenga asignaciones a lotes; un operador puede corregir su captura no confirmada. Una asignación o consumo confirmado no se edita. Registrar incidencias pendientes sobre errores históricos, sin cambiar saldos ni evidencias originales.

### 3. Recolección, lotes, QR y trazabilidad

- **FR-010**: Crear lotes solo desde generación disponible y conservar las relaciones y cantidades
  asignadas por origen. No asignar la misma masa a varios lotes. Mantener trazable la procedencia;
  no mezclar medidos, estimados y simulados en un mismo lote o proceso en esta propuesta de MVP.
- **FR-011**: Asignar identificador único y QR sin credenciales ni información sensible. La consulta
  del QR requiere los mismos permisos que cualquier consulta del lote.
- **FR-012**: Registrar movimientos y entregas con fecha, responsable, cantidad, destino, estado
  y relación con el lote. Distinguir eventos logísticos de asignaciones que consumen disponibilidad.
- **FR-013**: **Disponible del registro = generación vigente válida − masa asignada a lotes**.
  **Disponible del lote = masa asignada − consumos confirmados únicos** hacia procesos o destinos
  externos. Cada consumo se representa una sola vez, aunque tenga varios eventos logísticos.
  Una transferencia interna solo cambia custodia; no libera masa ya comprometida.
- **FR-014**: **No consumir más saldo que el disponible**, incluso ante concurrencia o reintentos.
  Repetir una misma operación conserva su resultado sin nueva afectación; alterar esa operación
  ya confirmada no reemplaza silenciosamente el resultado original.
- **FR-015**: Mostrar cronología y estado del lote. Estados: abierto con saldo,
  agotado sin saldo y cerrado cuando no quedan operaciones pendientes. Agotado no equivale
  a aprovechado. No cerrar con saldo disponible ni mover un lote cerrado. El operador confirma cierres; no hay reversiones históricas en el MVP; no existen transiciones implícitas que evadan esas reglas.

### 4. Aprovechamiento, compostaje y economía circular

- **FR-016**: Iniciar procesos con entradas orgánicas elegibles y disponibles; cada entrada
  confirmada consume saldo exactamente una vez y conserva su relación con lotes y generación.
- **FR-017**: Registrar inicio, observaciones, controles opcionales con unidad y fecha, y estado.
  Estados operativos: en proceso y finalizado; verificación del resultado es separada.
- **FR-018**: Registrar salidas positivas independientemente de las entradas, fecha y destino
  declarado. En operación real se exige medición propia; en demo se declara simulación explícita.
  La salida conserva la procedencia del proceso. Un proceso estimado puede conservar su salida
  estimada para trazabilidad, pero no puede acreditar aprovechamiento ni regularizarse en este MVP.
  **No asumir rendimiento, equivalencia 1:1 ni certificación de calidad del compost**.
- **FR-019**: Distinguir resultado pendiente de resultado confirmado con evidencia y responsable
  de validación. Una entrega no prueba automáticamente aprovechamiento y el compost obtenido
  no se suma a su entrada como dos aprovechamientos.
  Decisión Q3 aprobada: sumar una sola vez la masa de entrada identificada por lote cuando el proceso esté finalizado y el gestor valide pesaje independiente de salida, fecha, responsable y comprobante documental o registro verificable del destino. Sin cualquiera de esos elementos permanece pendiente. La salida de compost se informa por separado y nunca incrementa generación ni el numerador de aprovechamiento.
  Restricción CHK004: confirmar solo procesos medidos con entrada/salida medidas o procesos
  simulados como demostración. Rechazar confirmación de estimados sin cambiar procedencia,
  saldos ni historial. Confirmaciones estimadas anteriores, si existieran, se conservan como
  historial pero no se computan como A bajo esta regla; no se borran ni se reclasifican.

### 5. Indicadores ambientales, dashboard y reportes

- **FR-020**: Mostrar generación, distribución por material, saldo disponible, masa en proceso,
  aprovechamiento verificado y pendientes, con filtros por período de generación, área, material
  y procedencia, además de fecha de corte de seguimiento.
- **FR-021**: Generación G = suma de generación válida vigente del universo filtrado; distribución
  de material = generación del material / G × 100. Tasa de aprovechamiento = A / G × 100,
  donde A es masa de esos mismos orígenes acreditada hasta el corte bajo la validación de FR-019. Cada entrada del proceso aporta únicamente la parte de su cohorte incluida en los filtros; la fecha de validación debe ser igual o anterior al corte.
  No mezclar cohortes, sumar movimientos como generación ni usar masa de salida y entrada dos veces.
  Cuando G sea cero, mostrar «No calculable». Si existen pendientes, etiquetar tasa provisional.
- **FR-022**: Mostrar disponible, en proceso y pendiente de acreditación como conceptos distintos.
  No llamar «saldo disponible» a G − A ni interpretar masa pendiente como no aprovechable.
  Para compostaje, A suma entradas validadas según FR-019. Una entrega externa queda pendiente de acreditación: en este MVP no existe un flujo independiente de validación de reciclaje externo.
- **FR-023**: Mostrar fórmula, numerador, denominador, filtros, corte, procedencia y límites junto
  a los indicadores. Diferenciar datos ausentes, cero y fallo de consulta. Los gráficos tendrán
  alternativa textual o tabular; el color no será la única forma de comunicar categorías.
- **FR-024**: Exportar CSV del conjunto autorizado y filtrado, con procedencia, unidades, fechas
  e identificadores de origen. Incluir contexto de filtros y corte que permita reproducir los
  totales; conservar decimales y caracteres españoles y neutralizar textos que se interpreten
  como fórmulas al abrir el archivo en una hoja de cálculo.
- **FR-025**: Proporcionar navegación adaptable a móvil y escritorio, uso por teclado, etiquetas
  de campos y mensajes en español. Conservar datos no sensibles de formularios ante errores
  recuperables y comunicar carga, vacío, rechazo y resultado de cada operación.

### Key Entities *(include if feature involves data)*

- Institución, sede y área: ámbito y lugar de generación del piloto.
- Usuario y rol: identidad responsable y capacidades institucionales.
- Material: categoría ambiental y elegibilidad para destinos permitidos.
- Registro de generación: masa, origen del dato, fecha, responsable y estado de validación.
- Lote: agrupación trazable de masa asignada, identificador, saldo y estado.
- Movimiento: evento logístico o consumo de disponibilidad, responsable y destino.
- Proceso de compostaje: entradas orgánicas, controles, resultados y estado operativo.
- Resultado y evidencia: masa independiente, destino declarado y estado de verificación.
- Corrección auditada: motivo y cambios con referencia al registro original.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100 % de las operaciones de escritura del consultor y accesos no autorizados
  de los escenarios de prueba se rechazan sin revelar ni modificar información (FR-001–005).
- **SC-002**: El recorrido de 25 kg simulados, entrada de 20 kg y rechazo de 6 kg conserva
  5 kg disponibles y 25 kg generados, incluso tras recargar y volver a iniciar sesión
  (FR-006–018). Todos los valores de prueba permanecen identificados como simulados.
- **SC-003**: Cero consumos duplicados en reenvíos y cero saldos negativos ante operaciones
  simultáneas del escenario definido; todo intento fallido deja intactas las cantidades (FR-010–015).
- **SC-004**: El 100 % de totales de generación y distribución del conjunto de prueba coincide
  con el cálculo manual y el CSV con iguales filtros; aprovechamiento se verificará según FR-019
  con un conjunto cuyos orígenes y evidencias permitan calcular A de forma independiente (FR-019–024).
- **SC-005**: El 100 % de correcciones permitidas muestra responsable, motivo y valores anteriores
  y nuevos; ninguna modificación directa de un registro validado se acepta (FR-008–009).
- **SC-006**: Un operador de prueba completa registro y consulta sin ayuda oral usando teclado;
  los cinco recorridos muestran etiquetas, errores comprensibles y no exigen desplazamiento
  horizontal de la página a anchuras de 360 y 1280 píxeles (FR-025).
- **SC-007**: El catálogo excluye peligrosos y especiales del registro ordinario; los registros
  recuperados conservan categoría y procedencia; toda evidencia confirmada satisface FR-019 y ninguna
  salida se presenta como certificación (FR-004, FR-006, FR-017–019).

### Aceptación adicional de CHK004

1. Con G=25 kg medidos y entrada=20, salida propia=8 y evidencia completa, el gestor confirma:
   A=20, pendiente=5 y tasa=80 %; repetir la operación no duplica A y CSV coincide con el panel.
2. Con las mismas masas estimadas y evidencia completa, confirmar se rechaza; A=0,
   pendiente=25, saldo de lote=5 y procedencia estimada intacta. Una confirmación histórica
   estimada no incrementa indicadores ni CSV.
3. Una salida enviada como estimada a un proceso medido se rechaza sin finalizar ni crear salida.
   Tampoco se valida una salida histórica cuya procedencia contradiga la del proceso.
4. El flujo 25/20/8 simulado sigue funcionando como demostración; su A=20 solo pertenece
   al universo simulado, y un filtro medido no lo incluye. Sin evidencia válida no se confirma.

## Assumptions

- Una universidad piloto; el administrador prepara cuentas, espacios y catálogo antes de la demo.
  La selección institucional y su catálogo requieren validación del responsable del piloto;
  no se presenta un catálogo ficticio como oficial.
- Los estados y la prohibición de mezclar procedencias reducen ambigüedad del MVP;
  están implementados y se verifican en las pruebas registradas en docs/PRUEBAS.md.
- No se presupone conexión a equipos de pesaje. Las mediciones se introducen manualmente.
- Las pruebas usan datos declarados simulados; no se afirma que existan mediciones de campo.
- No hay flujo público por QR. La arquitectura futura no autoriza administrar varias instituciones.
- Los escenarios definen aceptación; la evidencia de sus ejecuciones está en docs/PRUEBAS.md,
  no se infiere cumplimiento solamente por aparecer en esta especificación.
- El alcance de validación verificable del MVP es compostaje. Las entregas externas conservan trazabilidad y estado pendiente, sin asumir aprovechamiento por una recepción. A1 aprobado por el usuario el 2026-11-15. El dashboard identifica explícitamente aprovechamiento confirmado por compostaje, no aprovechamiento total institucional.

## Lo que NO se va a construir en esta iteración (Non-Goals)

- IA, chatbot, clasificación por fotografía, pronósticos o recomendaciones autónomas.
- IoT, básculas conectadas, pesaje automático, microservicios y colas distribuidas.
- Campañas, metas, comercio, pagos, gestión de cultivos o logística agrícola.
- Gestión operativa de peligrosos, certificación legal, calidad agronómica certificada o huella
  de carbono certificada. El catálogo ordinario no sustituye protocolos ambientales revisados.
- Administración multiinstitución, portales públicos por QR y aplicaciones móviles nativas.
- PDF en el alcance base: es una mejora futura; esta especificación exige CSV.
- Eliminación silenciosa de registros validados, generación de mediciones o atribuciones ficticias.

- Reversiones históricas de consumos o lotes cerrados y validación de aprovechamiento externo distinta de compostaje quedan fuera del MVP; se conserva trazabilidad e incidencias.

A2 aprobado: correcciones de generación exclusivamente sin asignaciones ni consumos; incidencias para errores históricos. El panel separa generado, entregado externamente, pendiente y aprovechamiento confirmado por compostaje.

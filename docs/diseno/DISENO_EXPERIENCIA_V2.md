# EcoGest 360 Intelligence — diseño de experiencia V2

Estado: dirección aprobada el 2026-11-16; fase A implementada, restantes vistas solo diseñadas. Fuente: brief maestro y
[spec V2](../../specs/002-ecogest-intelligence/spec.md). Q1–Q3 aprobadas; gasto y credenciales IA no habilitados.
Las referencias visuales son descripciones; no hay imágenes de referencia disponibles que se hayan inspeccionado.

## Concepto y arquitectura de información

Una consola que conecta **evidencia → hipótesis → acción → evaluación**. La calidad premium
se comprobará por claridad de decisiones, contexto compartido y acceso al origen de cada cifra,
no por tarjetas decorativas. Las funciones operativas existentes siguen accesibles.

Navegación lateral agrupada:
- Analizar: Observatorio, Simulador, Planes de acción.
- Operar: Registros, Trazabilidad, Compostaje, Incidencias.
- Apoyo: Asistente IA.
- Administrar: Institución (solo administrador).

Inicio tras login: Observatorio. Pie lateral: institución, usuario, rol y cerrar sesión.
No ocultar Incidencias aunque no aparezca en la lista corta del brief. Trazabilidad reemplaza
la etiqueta Lotes, conservando identificación y accesos QR. Institución conserva configuración.
Cada pantalla tiene título, descripción útil y una acción primaria según rol. Navegar no ejecuta acciones.

Contexto común: período de generación, área, material, procedencia y corte. Siempre se ve la
procedencia; proponer iniciar en Medido y mostrar vacío si no existe, con acceso explícito a
Simulado. No cargar simulados automáticamente para llenar la pantalla. La vista «Todas»
desglosa procedencias y deshabilita comparaciones/escenarios hasta elegir una.

## Sistema visual

| Token propuesto | Valor | Uso |
| --- | --- | --- |
| Bosque | #12382F | Navegación, titulares destacados |
| Jade | #167C68 | Acciones principales, series de datos |
| Salvia | #DCEBDB | Superficies secundarias, selección |
| Marfil | #F7F9F5 | Fondo de contenido |
| Grafito | #25332E | Texto principal |
| Ámbar | #E5A24D | Atención, con texto grafito y etiqueta |
| Blanco | #FFFFFF | Tarjetas y texto sobre superficies oscuras |
| Error propuesto | #A12A32 | Error con icono, título y explicación |

Tipografía: pila local Inter si está disponible, Segoe UI, sans-serif; sin descarga externa
obligatoria. Cuerpo 16 px/1.5, metadatos 13–14 px, títulos 28–36 px desktop y 24–28 móvil;
valores 32–40 px con números tabulares. No texto esencial menor de 12 px.
Espaciado 4/8/12/16/24/32/48 px; radios 12 px en tarjetas, 8 px en controles; bordes sutiles,
sombra solo para superposiciones. Iconos SVG de una familia propia de trazo consistente.
Transiciones 120–180 ms para orientación; suprimir movimiento con preferencia reducida.
Gráficos SVG con leyenda, valores textuales y tabla equivalente. No animar cifras como si fueran mediciones nuevas.

Contraste se verificará al implementar: objetivo 4.5:1 texto normal y 3:1 texto grande/controles;
no se da por aprobado por elegir esta paleta. Ámbar no se usa como texto sobre blanco.
Foco visible de alto contraste; targets táctiles objetivo ≥44×44 px; zoom sin pérdida de operación.

## Composición responsive

1280 px: barra lateral 224 px, padding de contenido 24 px, rejilla de 12 columnas y gap 16/24.
768 px: menú plegable, tarjetas en dos columnas cuando sus textos caben; detalle de una columna.
390/360 px: cabecera compacta, menú modal accesible, padding 16 px y tarjetas apiladas.
Tablas anchas dentro de región desplazable etiquetada o tarjetas por fila, sin overflow horizontal
de página. Acciones no dependen del hover. Orden de lectura mantiene evidencia antes de sugerencia.
Panel IA lateral de 360 px solo si no comprime el contenido: en 1280 se superpone con fondo y
control de foco; alternativa «Abrir pantalla completa». En móvil siempre pantalla completa.
Al cerrar panel, devolver foco al botón de apertura. Menú/dialogo soporta Escape y foco acotado.

## Wireframe 1 — Observatorio (US1)

```text
DESKTOP
[nav 224] [Observatorio / institución             Consultar asistente]
          [Contexto: fechas | área | material | procedencia | corte]
          [Generados] [Compostaje acreditado] [Pendientes] [Tasa]
          [Serie generación + comparar período     ][Hallazgos]
          [Tabla accesible / fuente                 ][Ver evidencia]
          [Áreas contribuyentes + métrica elegida   ][Simular / Crear plan]
          [Fórmula, cobertura, actualización y límites | CSV]
MÓVIL
[Menú] [Observatorio] [Ayuda]
[Procedencia / período siempre visibles]
[Editar filtros] [chips activos]
[KPI] [KPI] [KPI] [KPI]
[Tendencia + tabla desplegable]
[Hallazgo → evidencia → acción]
[Ranking] [Exportar] [Fórmula y límites]
```

KPI: título específico, masa/unidad, fórmula consultable, comparación solo si válida. Una caída
de generación no recibe automáticamente un sello de «éxito». Serie agrupa fechas de generación;
los días sin registros se marcan sin registro, no como mediciones cero. Comparador según Q1.
Ranking selecciona generado/pendiente; orden y universo explícitos. Tarjeta de hallazgo incluye
regla, datos usados, fecha, enlace a registros y acciones permitidas. «Crear plan» solo gestor.
Sin datos: explicar filtros y ofrecer quitarlos; no dibujar serie plana inventada.

## Wireframe 2 — Trazabilidad y pasaporte (US2)

```text
DESKTOP
[Buscar lote / filtros] → [Pasaporte del lote #ID | procedencia | estado]
                          [Asignado | disponible | consumido]
                          [Orígenes] → [Traslados] → [Destinos ramificados]
                          [Cronología y responsables  ][QR + identificación]
                          [Proceso vinculado → evidencia → verificación]
                          [Acciones según rol / Registrar incidencia]
MÓVIL
[Volver] [Lote #ID] [Estado + procedencia]
[Saldo y masa asignada]
[Etapas verticales con ramas desplegables]
[Eventos con kg / efecto en saldo / responsable / fecha]
[QR] [Evidencias autorizadas] [Acciones]
```

Pasaporte no es certificado. Mostrar «No registrado» si falta un dato. Una etapa pendiente se
presenta como posibilidad no ocurrida; no tiene fecha inventada ni check de completada.
Separar fecha del evento y fecha de registro si existen ambas. Identificador de proceso y
asignaciones muestran cuándo una evidencia es compartida. No prorratear compost obtenido
sin pesaje propio. Filtros de Observatorio viajan como contexto, pero el pasaporte presenta
historia completa autorizada del lote y explica que puede contener otros orígenes.

## Wireframe 3 — Simulador (US3)

```text
DESKTOP
[SIMULACIÓN / no modifica registros] [Contexto y momento de captura]
[Elegir hipótesis + alcance por área]
[Controles: valor en kg + límite elegible] [Base       | Escenario]
[Supuestos y fórmula                  ] [G, A, tasa | G', A', tasa']
[Recalcular] [Restablecer]               [Diferencias absolutas]
[Ver fuentes] [Preparar plan: solo gestor, sin guardado automático]
MÓVIL
[SIMULACIÓN] [Contexto]
[Hipótesis] [Cantidad con unidad / máximo]
[Calcular]
[Base] [Escenario] [Diferencias]
[Supuestos / fuentes] [Preparar plan]
```

Entrada numérica operable por teclado, no solo slider; valor negativo o mayor al elegible
muestra error junto al campo. Sin línea base: no habilitar cálculo. Con base desactualizada:
mostrar aviso y exigir recarga antes de proponer plan. Escenario no guardado: avisar al salir
si se perderán cambios, sin persistencia silenciosa en almacenamiento del navegador.
«Preparar plan» transfiere hipótesis como sugerencia separada de la evidencia base; el gestor
revisa formulario y confirma. Ningún botón «Aplicar al sistema».

## Wireframe 4 — Planes (US4)

```text
DESKTOP
[Planes de acción] [Nuevo plan: gestor]
[Estado | área | responsable] [Lista: problema, meta, plazo, estado]
[Detalle: problema + hallazgo de origen]
[Acción / responsable / plazo] [Base | meta | posterior observado]
[Seguimiento cronológico] [Evaluar / cambiar estado con motivo]
MÓVIL
[Filtros] [Fichas resumidas]
[Plan → problema → fuentes → acción]
[Responsable / plazo / estado]
[Base] [Meta] [Resultado o No evaluable]
[Seguimientos] [Acción permitida]
```

Crear: cuatro pasos cortos — problema/evidencia, acción/responsable, indicador/meta/plazo,
revisión y confirmación. No duplicar formulario completo por tarjeta. Progreso operativo
(estado/actividades) separado del resultado ambiental. No porcentaje decorativo por casillas.
Mostrar «Meta alcanzada observada» solo con cálculo elegible, nunca «Éxito causado por el plan».
Meta de reducción en kg o aumento de tasa en puntos porcentuales, según indicador elegido;
meta no puede cambiar de unidad a mitad de comparación. Ediciones auditadas, cancelación con motivo.

## Wireframe 5 — Asistente (US5)

```text
[Asistente IA] [Disponible / No disponible]
[Mis datos | Explicar | Proponer acciones]
[Contexto fijado: institución, área, período, procedencia, corte]
[Pregunta del usuario]
[Datos verificados: valor + referencia]
[Interpretación IA / límites]
[Fuentes internas consultables]
[Escribir pregunta] [Enviar] [Limpiar conversación]
```

La vista lateral usa los mismos elementos y el mismo contrato de contexto. Preguntas sugeridas:
«¿Qué compone lo pendiente?», «Explica la fórmula», «Sugiere una intervención para este hallazgo».
No preguntar por supuestas anomalías si no existe hallazgo. Advertir envío externo de contexto
mínimo antes de la primera consulta y ofrecer consulta determinista sin IA.
Respuesta anterior conserva sus filtros aunque cambien los actuales. Nueva sesión limpia historial.
No mostrar credenciales ni controles de configuración técnica en el flujo del usuario final.
Sin servicio: tarjeta verificable de métricas y aviso; no burbuja fingida atribuida a IA.

## Operación existente y estados

Registros: filtros arriba, tabla al centro y formulario solo bajo acción «Registrar generación»
para operador. Detalle/historial accesibles desde fila. Mantener corrección autorizada y validación.
Compostaje: lista de procesos con entrada/salida/estado; detalle concentra controles, evidencia
y validación por rol, sin repetir todos los formularios en la lista. Institución conserva altas
y mantenimiento; Incidencias permanece accesible globalmente y desde detalle.

| Pantalla | Carga | Vacío / insuficiente | Error / permiso | Confirmación |
| --- | --- | --- | --- | --- |
| Observatorio | Esqueleto sin cifras y estado textual | Filtros y cobertura explicados | Reintentar sin perder contexto; sin datos ajenos | Filtros aplicados y corte visible |
| Pasaporte | Estructura sin eventos falsos | Etapas sin registro explícitas | No encontrado/no disponible, sin revelar otra institución | Solo acciones operativas autorizadas |
| Simulador | Cargando base, calcular deshabilitado | Explicar por qué E o base no permiten hipótesis | Error junto a entrada; conservar hipótesis | Resultado hipotético, nunca guardado operativo |
| Planes | Lista/detalle en espera | Crear disponible solo al gestor | Conflicto exige recargar; prohibición explícita | Autor/fecha/estado persistido |
| Asistente | Espera cancelable; impedir doble envío | Evidencia insuficiente y fuentes disponibles | No disponible, cuota o respuesta inválida | Respuesta vinculada al contexto original |
| Operación MVP | Estado Guardando | Lista vacía con acción por rol | Preservar entrada segura y clave de reintento | Resultado actualiza saldo una sola vez |

## Demostración propuesta y aceptación visual

1. Elegir explícitamente una cohorte simulada; Observatorio muestra datos disponibles y límites.
2. Abrir hallazgo y registro, después su pasaporte; distinguir traslado y consumo.
3. Simular una hipótesis elegible; comprobar que panel original permanece igual.
4. Gestor prepara un plan, revisa y guarda; mostrar meta pendiente sin inventar cumplimiento.
5. Asistente explica fuentes y sugiere acciones; repetir sin servicio y mostrar funcionamiento manual.
6. Comparar resultados posteriores solo si existen datos comparables; de lo contrario «No evaluable».

Evaluar en 360/390/768/1280 px, teclado, zoom y movimiento reducido. Una persona debe poder
identificar procedencia, fuente y siguiente acción sin ayuda oral; registrar tiempo y errores.
Estos wireframes son antecedentes del diseño. A–E están implementadas localmente; la prueba pagada IA y la aceptación humana siguen pendientes.


## Estado construido — orden final 2026-11-16

Pasaporte, Simulador, Planes y Asistente reutilizan verde bosque/marfil, CSS Modules,
formularios accesibles y estados explícitos. Rutas /simulador, /planes, /asistente,
/registros y /lotes conservan filtros; recarga y atrás del navegador restauran el contexto.
Las fuentes del pasaporte permiten explorar la cohorte del origen, avisando que puede
incluir otros registros. Observatorio abre evidencia y escenario; el escenario propone un
plan que el gestor revisa; planes permiten volver a consulta contextual del asistente.

Planes utilizan un único formulario de propuesta y un detalle por selección, sin duplicar
formularios en cada tarjeta. Edición de meta/responsable y auditoría se despliegan; el
resultado ambiental se separa del seguimiento. Responsable inactivo se advierte. Las metas
son valores absolutos del indicador (kg o %), la diferencia de tasas usa puntos porcentuales.

Asistente: tres modos, ejemplos que enfocan la pregunta por teclado, fuentes locales,
metodología sin servicio y respuesta estructurada verificable. El modelo selecciona códigos
validados; no se renderiza texto libre con cifras inventadas. No ofrece conversación abierta
fuera del catálogo. Conversación efímera; respuesta anterior conserva contexto y deshabilita
acciones obsoletas al cambiar filtros. Los envíos tardíos se descartan, la espera UI se acota
sin reintentos automáticos. La IA nunca inicia decisiones humanas. Capturas en
`evidencias/v2/asistente` muestran el modo local real, no respuestas falsas de OpenAI.

Las capturas reales en pasaporte/simulador/planes/asistente cubren 360/390/768/1280; resultados
finales y límites en docs/PRUEBAS.md. El guion audiovisual existente se amplió, no se creó otro.

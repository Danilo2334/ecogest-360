# ?ndice de documentaci?n ? EcoGest 360 Intelligence

La ra?z de docs/ contiene ?nicamente este ?ndice y los dos registros principales:
[DECISIONES.md](DECISIONES.md) y [PRUEBAS.md](PRUEBAS.md). Se conservan **24 Markdown**
en total, incluidos los antecedentes. Para instalar y ejecutar la aplicaci?n, consultar
el [README principal](../README.md).

## Fuentes oficiales SDD

La [constituci?n vigente](../.specify/memory/constitution.md) permanece en .specify/.
Los artefactos oficiales siguen separados en specs/:

- MVP: [especificaci?n](../specs/001-ecogest-mvp/spec.md),
  [plan](../specs/001-ecogest-mvp/plan.md) y [tareas](../specs/001-ecogest-mvp/tasks.md).
- V2: [especificaci?n](../specs/002-ecogest-intelligence/spec.md),
  [plan](../specs/002-ecogest-intelligence/plan.md) y [tareas](../specs/002-ecogest-intelligence/tasks.md).

Solo se actualizaron las rutas documentales afectadas por la organizaci?n; no se cambiaron
reglas, requisitos, versiones constitucionales ni estados de las tareas.

## Dise?o vigente ? diseno/

- [DISENO_EXPERIENCIA_V2.md](diseno/DISENO_EXPERIENCIA_V2.md): navegaci?n, pantallas,
  estados, componentes y criterios visuales de la V2.

## Entrega y evaluaci?n ? entrega/

- [AUDITORIA_FINAL.md](entrega/AUDITORIA_FINAL.md): auditor?a V1 y adendas; conserva
  los estados hist?ricos. Los resultados posteriores se consultan en PRUEBAS.
- [DEMO_ACADEMICA.md](entrega/DEMO_ACADEMICA.md): guion V2 y recorrido operativo V1 alternativo.
- [REGISTRO_DEMO_HUMANA.md](entrega/REGISTRO_DEMO_HUMANA.md): hoja de CHK013, pendiente de ejecuci?n humana.
- [CHECKLIST_ENTREGA.md](entrega/CHECKLIST_ENTREGA.md): inventario y pendientes de entrega.
- [MATRIZ_CUMPLIMIENTO_DOCENTE.md](entrega/MATRIZ_CUMPLIMIENTO_DOCENTE.md): seis criterios docentes,
  evidencias y l?mites; conserva antecedentes V1.
- [ENMIENDA_CONSTITUCION_SVG.md](entrega/ENMIENDA_CONSTITUCION_SVG.md): evidencia de ratificaci?n
  de la enmienda 1.1.0; no reemplaza la constituci?n oficial.

## Evidencias y escenarios ? evidencias/

- [DATOS_DEMO_OBSERVATORIO.md](evidencias/DATOS_DEMO_OBSERVATORIO.md): preparaci?n y l?mites
  de la cohorte reproducible, exclusivamente simulada.
- [Capturas existentes](evidencias/) y [capturas V2](evidencias/v2/): se conservan sus rutas
  y contenido; no sustituyen la demostraci?n humana.

Las dos consultas reales de OpenAI est?n documentadas en PRUEBAS con tokens, costo local
calculado y presupuesto autorizado. Se ejecutaron desde Django, sin validar el recorrido
completo del navegador con IA real. El servicio qued? desactivado y no se autoriza m?s consumo.

## Antecedentes ? historico/

Estos documentos conservan el estado de su fecha. No son la fuente principal de requisitos
ni instrucciones nuevas para ejecutar comandos, habilitar servicios o ampliar el alcance.

- [01_VISION_Y_ALCANCE_ECOGEST360.md](historico/01_VISION_Y_ALCANCE_ECOGEST360.md): visi?n inicial amplia.
- [02_CONSTITUCION_PROPUESTA_ECOGEST360.md](historico/02_CONSTITUCION_PROPUESTA_ECOGEST360.md): borrador anterior a la ratificaci?n.
- [03_ALCANCE_MVP_ECOGEST360.md](historico/03_ALCANCE_MVP_ECOGEST360.md): insumo de alcance V1, subordinado a spec.md.
- [04_PLAN_DE_EJECUCION_Y_EVIDENCIAS.md](historico/04_PLAN_DE_EJECUCION_Y_EVIDENCIAS.md): plan orientativo y evidencias iniciales.
- [DIAGNOSTICO_V2_PRELIMINAR.md](historico/DIAGNOSTICO_V2_PRELIMINAR.md): diagn?stico Brownfield previo a la implementaci?n.
- [INFORME_FASE_A_V2.md](historico/INFORME_FASE_A_V2.md): primer incremento del Observatorio.
- [INFORME_REFINAMIENTO_OBSERVATORIO.md](historico/INFORME_REFINAMIENTO_OBSERVATORIO.md): refinamiento, fallos y capturas de aquel hito.
- [PROMPT_MAESTRO_ECOGEST_360_INTELLIGENCE_V2.md](historico/PROMPT_MAESTRO_ECOGEST_360_INTELLIGENCE_V2.md): brief de origen.
- [PREPARACION_GITHUB.md](historico/PREPARACION_GITHUB.md): procedimiento propuesto y estado de Git en aquel momento.
- [PR_MVP_PROPUESTO.md](historico/PR_MVP_PROPUESTO.md): texto propuesto; no demuestra publicaci?n o revisi?n.
- [RESUMEN_CAMBIOS_PARA_COMMIT.md](historico/RESUMEN_CAMBIOS_PARA_COMMIT.md): conciliaci?n de autor?as declaradas y cambios del hito.

## Material docente original ? plantillas/

- [plantilla_constitucion_sdd.md](plantillas/plantilla_constitucion_sdd.md).
- [prompt_spec_template.md](plantillas/prompt_spec_template.md).

Las dos plantillas se trasladaron sin modificar su contenido. No se eliminaron ni fusionaron
antecedentes o evidencias ?nicas. Las referencias en instrucciones, documentaci?n y SDD
se actualizaron; no se necesit? una excepci?n para conservar otro Markdown en la ra?z.
CHK013, revisiones aut?nticas, entrega individual en Campus UCC y cinco tareas TDD
hist?ricamente parciales conservan su estado real.

# Matriz de cumplimiento — seis criterios docentes

**Fuente:** títulos y descripciones aportados en esta conversación a partir de
`Criterios_evaluacion_proyecto_final_SDD (1).pdf`, página 2. El PDF todavía no está físicamente
en el repositorio; el agente no lo ha inspeccionado directamente. Esta matriz reemplaza la
agrupación provisional anterior por los seis títulos exactos confirmados por el usuario.

Los estados son una evaluación técnica de las evidencias disponibles, no una calificación
docente. No se inventan porcentajes, ponderaciones ni resultados. «Cumple» se limita al alcance
indicado en la fila; no significa aprobación académica definitiva.

| N.º / criterio oficial | Qué evalúa | Evidencias y ubicación | Cumplimiento respaldado | Pendientes | Estado | Acciones para completar la entrega |
| --- | --- | --- | --- | --- | --- | --- |
| 01 — Artefactos SDD | Constitución, especificaciones, plan y tareas | `.specify/memory/constitution.md`; `specs/001-ecogest-mvp/{spec,plan,tasks}.md`; `docs/entrega/ENMIENDA_CONSTITUCION_SVG.md`; commit `58bab1f` | Constitución 1.1.0 ratificada el 2026-11-15; cinco módulos especificados; regla CHK004 aprobada y conciliación de rama/plan documentada | Cinco tareas TDD históricamente parciales; cierre registrado en `d29b01b`; conciliación documental actual pendiente de commit | Parcial | Incorporar cambios aprobados al control de versiones cuando se autorice. Conservar T008/T014/T019/T026/T032 parciales, sin fabricar secuencia histórica |
| 02 — Aplicación funcional | Cumplimiento de requisitos y ejecución del sistema | `backend/`; `frontend/src/`; `compose.yaml`; `frontend/tests/e2e/vertical.spec.ts`; `docs/entrega/AUDITORIA_FINAL.md` | Flujo local generación→lote→compostaje→validación→panel/CSV ejecutado; PostgreSQL persistente; estimados sin acreditación, simulados separados | CHK013 sin ejecución humana; catálogo real no validado; instalación independiente no comprobada | Parcial | Ejecutar recorrido humano y registrar resultados; verificar reproducción por otra persona y alcance del catálogo piloto. No presentar la demo como mediciones ambientales reales |
| 03 — Calidad técnica | Código legible, validaciones y manejo de errores | `backend/core/{validation,idempotency,permissions,errors}.py`; servicios de dominio; `backend/tests/test_audit.py`; `frontend/tests/form.test.tsx`; `docs/PRUEBAS.md` | Decimales, permisos, CSRF, transacciones e idempotencia probados; defectos de nulos/adjuntos/fecha corregidos; TypeScript y build correctos; código separado por dominio | Tipos genéricos `Row`, transporte REST centralizado y listados sin paginación son límites documentados; no hay certificación de seguridad ni rendimiento global | Cumple | Presentar validaciones y manejo de errores con sus pruebas; revisión humana final de legibilidad. Mantener los límites explícitos, sin añadir funciones ajenas al MVP |
| 04 — Trabajo colaborativo | Ramas, commits individuales y pull requests | Rama `feat/001-ecogest-mvp`; commits `58bab1f`, `fd90a7d`, `d680fb3`, `d29b01b`; `docs/historico/PREPARACION_GITHUB.md` | Cuatro commits: dos autores Danilo y dos Francisco, conforme a la aclaración del usuario; main con base común válida | Sin remoto, PRs, revisiones ni confirmación individual de aportes desde ambas cuentas | Parcial | Confirmar aportes reales por ambos integrantes; publicar solo tras autorización y registrar PRs y revisiones auténticas. No reescribir historial ni confundir autoría con prueba independiente de colaboración |
| 05 — Pruebas y verificación | Evidencia de pruebas de funcionalidades clave | `backend/tests/`; `frontend/tests/`; `docs/PRUEBAS.md`; capturas en `docs/evidencias/` | Última ejecución: 30 Django/PostgreSQL, 5 Vitest y 3 Playwright aprobadas; 38 en total, 0 fallidas finales. Tres fallos iniciales de CHK004 preservados; cobertura de masas, permisos, concurrencia, procedencia e informes | Sin evidencia TDD histórica completa en cinco tareas; cámara QR y prueba humana no ejecutadas; cobertura no exhaustiva | Cumple | Conservar comandos, resultados y límites; adjuntar evidencia a la entrega y ejecutar CHK013 por separado. No sustituir historia TDD ni declarar pruebas no realizadas |
| 06 — Documentación y demo | README, decisiones y presentación clara | `README.md`; `.env.example`; `docs/DECISIONES.md; docs/PRUEBAS.md; docs/entrega/AUDITORIA_FINAL.md; docs/entrega/DEMO_ACADEMICA.md; docs/entrega/REGISTRO_DEMO_HUMANA.md`; capturas simuladas | Instalación, ejecución, fórmulas, decisiones y guion documentados; hoja humana preparada y vacía | Demo humana y su registro pendientes; aprobación final de presentación; entregas individuales en Campus UCC no realizadas | Parcial | Completar hoja con persona/fecha/navegador/resultados/capturas/dificultades; explicar límites de simulación. Cada integrante debe cargar su entrega en Campus UCC y conservar constancia |

## Colaboración pendiente de confirmación y revisión

Los metadatos coinciden con la aclaración del usuario sobre el trabajo de cada integrante.
No prueban por sí solos quién realizó el trabajo ni constituyen una revisión independiente.
Ambos integrantes deben confirmar sus aportes desde sus cuentas reales. Las revisiones y PRs
siguen pendientes. No se modificaron autores, fechas ni historial durante esta preparación.

## Entrega individual y alcance de la fuente

Según la información aportada por el usuario de la página 8 del mismo PDF, **cada integrante
debe cargar la entrega mediante Campus UCC**. Es independiente del repositorio compartido.

- Danilo: carga y constancia pendientes.
- Francisco: carga y constancia pendientes.
- Plazo, formato de archivos y enlace del Campus: no proporcionados; no se presuponen.

Los seis títulos ya están confirmados por el usuario; no queda pendiente inventarlos ni
renombrarlos. Sigue pendiente disponer del PDF completo para cotejar instrucciones adicionales,
pesos y formato exacto. El PDF fue compartido y revisado en la conversación según la aclaración
recibida; no se atribuye una consulta personal al estudiante ni una inspección directa al agente local.
Las correcciones técnicas autorizadas de CHK004 ya se ejecutaron; no se reconstruye el MVP
ni se repiten pruebas por este cambio exclusivamente documental.


## Adenda de cierre local V2 — 2026-11-16

Las filas anteriores conservan el estado histórico de auditoría/preparación V1. Para el
estado técnico vigente consultar README, specs/002-ecogest-intelligence y docs/PRUEBAS.md:
A–E integradas, 69 pruebas backend aprobadas, regresión de navegador 9/9 más 3 recorridos
posteriores de rutas y responsive. OpenAI implementado con mocks, sin gasto real ni activación.
Migraciones completas verificadas en PostgreSQL vacío aislado; reproducción por otra persona
sigue pendiente. La guía audiovisual existente incorpora V2 y preserva alternativa V1.

Se mantienen los seis criterios oficiales sin porcentajes de nota: Artefactos SDD **Parcial**
por evidencias históricas incompletas y cierres humanos; Aplicación funcional **Parcial** por
CHK013 y validación independiente; Calidad técnica **Cumple en alcance probado**;
Trabajo colaborativo **Parcial** sin revisión auténtica comprobada en esta ejecución;
Pruebas y verificación **Cumple en alcance automatizado probado**, sin extrapolar a llamada
OpenAI real; Documentación y demo **Parcial** hasta evidencia humana y entrega.
El repositorio privado y PR #1 son antecedentes indicados por el equipo, no nuevas operaciones
ni revisiones verificadas aquí. Esta ejecución V2 no hizo push, PR, merge ni consulta remota.
No se reatribuyeron autores. Campus UCC y PDF físico siguen pendientes según registro previo.

### Actualización posterior: prueba real de OpenAI

El 2026-11-16 se verificaron dos consultas reales desde Django, con fuentes y metodología
ambiental del escenario simulado. Consumo: 1.862 tokens de entrada y 61 de salida; costo
local calculado USD 0,00538700, presupuesto autorizado USD 0,12. No es facturación oficial.
El servicio quedó desactivado. Evidencia y límites en [PRUEBAS.md](../PRUEBAS.md).
Esta comprobación amplía el alcance probado del criterio 05; no altera los estados docentes,
no acredita el flujo completo del navegador con OpenAI real ni cierra CHK013, colaboración,
entrega individual o las cinco tareas TDD históricamente parciales. Las afirmaciones anteriores
de ausencia de consumo real describen el momento previo a esta prueba.

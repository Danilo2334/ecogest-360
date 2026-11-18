# Auditoría técnica y preparación de entrega — 2026-11-15

## Dictamen

**Apto para una demostración local supervisada con datos simulados; todavía no para declarar
la entrega académica cerrada ni para operación con mediciones reales.** Se conservaron rama,
identidades, datos y constitución. No se crearon commits, remotos ni publicaciones.

Se revisaron constitución, especificación, plan, tareas, README, decisiones, pruebas,
las dos plantillas docentes locales y la visión/alcance propuestos. El PDF de criterios de
evaluación mencionado en la conversación no está en el repositorio: no se certifica su cumplimiento.

## Los 13 criterios

Resultados de esta revisión técnica, no aprobación de la profesora ni firma del responsable
ambiental. Las casillas originales conservan su semántica de revisión humana de requisitos.
**Estado actualizado tras cierre CHK004: 12 aprobados técnicamente y 1 pendiente (CHK013).**
La auditoría inicial tenía 11/13; sus ejecuciones y fallos se conservan en docs/PRUEBAS.md.

| Criterio / requisito | Evidencia verificable | Resultado | Riesgo o límite |
| --- | --- | --- | --- |
| CHK001: confirmación ordinaria frente a validación ambiental, FR-005 | spec.md §Clarifications; core/views.py dispatch; test_security.py; test_compost.py; test_audit.py test_consultant_cannot_write_any_action | Aprobado | Roles sin herencia ambiental; la autorización no sustituye capacitación del usuario |
| CHK002: generado, asignado, consumido, disponible y acreditado, FR-013/021/022 | traceability/services.py create/consume; reports/selectors.py; test_vertical.py; test_reports.py | Aprobado | Disponible global y disponible de un registro son distintos; las categorías no se suman entre sí |
| CHK003: corrección e incidencia histórica, FR-009 | waste/services.py correct; core/views.py incidents; test_security.py test_correction_audited_and_incident; test_concurrency.py | Aprobado | Incidencias pendientes no tienen resolución/reversión en el MVP |
| CHK004: evidencia y condiciones verificables, FR-018/019 | compost/services.py evidence/verify/finalize; test_compost_provenance.py (6 casos); test_compost.py; test_audit.py | Aprobado | Regla aprobada: medidos con salida propia y evidencia; simulados solo demo; estimados sin acreditación. Panel y CSV excluyen confirmaciones estimadas históricas sin borrar historial. El gestor debe examinar autenticidad y contenido de la evidencia real |
| CHK005: salida independiente de entradas, FR-018/021 | compost/models.py Output separado de Input; reports/selectors.py solo ConsumptionSource; test_vertical.py | Aprobado | 20 de entrada y 8 de salida acreditan 20, nunca 28; no se certifica rendimiento/calidad |
| CHK006: concurrencia, reenvío y fallo parcial | core/idempotency.py; test_concurrency.py; test_security.py test_idempotency_conflict_and_rollback | Aprobado | Pruebas con conexiones PostgreSQL independientes; no garantizan toda combinación bajo carga de producción |
| CHK007: procedencia simulada de demo | Process.provenance, Output.provenance; serialize de compost; test_compost.py; tests/e2e/vertical.spec.ts | Aprobado | Evidencias y validaciones heredan contexto del proceso; texto documental aún requiere revisión, no basta llamar real a un archivo |
| CHK008: cohorte, corte y corrección vigente | spec.md Clarifications; reports/selectors.py limitations; test_compost.py test_cohort_sources_and_nonorganic y prueba de corte | Aprobado | No reconstruye estados/correcciones históricos completos; se declara en panel y CSV |
| CHK009: 25/20/8 y denominador cero | test_vertical.py; test_security.py consulta vacía; frontend/tests/reports.test.tsx | Aprobado | Universo aislado: G=25, A=20, pendiente=5, tasa=80 %; vacío es No calculable |
| CHK010: catálogo piloto como dependencia | spec.md Assumptions; core/management/commands/seed_demo.py; README | Aprobado | Catálogo demostrativo identificado; su aprobación institucional real sigue pendiente |
| CHK011: entregas externas | A1 aprobado en spec.md y docs/DECISIONES.md; test_reports.py test_external_delivery_not_accredited | Aprobado | Entrega consume saldo pero no acredita aprovechamiento externo |
| CHK012: acceso QR, evidencias y CSV | test_security.py aislamiento; test_compost.py descarga privada; test_audit.py test_qr_image_and_authorized_lookup | Aprobado | PNG generado, lookup UUID autorizado y anónimo rechazado. No se ejecutó decodificación óptica del QR ni escaneo con cámara |
| CHK013: teclado, errores y tamaños medibles | FR-025/SC-006; Playwright vertical.spec.ts; Vitest form.test.tsx | Pendiente | Automatización pasa a 360/1280 px, foco y teclado; falta operador humano sin ayuda oral y evaluación de accesibilidad más amplia |

Rutas backend relativas a backend/, frontend relativas a frontend/. Reejecutar suites con
los comandos de README. Los resultados de ejecución de esta auditoría están en docs/PRUEBAS.md.

## Defectos confirmados y correcciones

1. **Evidencia incompleta aceptada:** `null` en receptor/descripción se convertía en el texto
   `None`; referencia `null` aparentaba estar presente. La prueba nueva obtuvo 201 donde
   debía obtener 400 y persistió tres evidencias inválidas en la base de tests. Se exige tipo
   texto y contenido no vacío antes de guardar. Regresión: test_null_required_evidence_is_rejected.
2. **Error interno de adjunto:** multipart con campo distinto de `file` producía
   MultiValueDictKeyError. Ahora solo se admite un archivo bajo `file` en la acción de evidencia;
   otros campos o múltiples archivos producen 400. Regresión: test_unexpected_upload_field_is_rejected.
3. **Fecha predeterminada incorrecta:** today() recortaba fecha UTC y adelantaba el día en
   Colombia por la noche. Regresión date.test.tsx falló (16 en vez de 15) antes del arreglo;
   ahora usa componentes de fecha local. Playwright configura explícitamente America/Bogota.
   No se corrigieron registros históricos de demostración de forma silenciosa.
4. El primer test de QR cerraba FileResponse y también la conexión transaccional del cliente,
   afectando el siguiente fixture. Se corrigió el test para consumir el PNG sin cerrar la respuesta
   dentro del TestCase. No era pérdida de datos de la aplicación. Además, un recorrido E2E
   navegaba antes de que terminara logout; se espera la pantalla de acceso antes del nuevo login.

Las pruebas de regresión anteriores se ejecutaron antes y después del arreglo. Esto no cambia
la falta de secuencia TDD histórica de T008/T014/T019/T026/T032.

## Discrepancias y límites abiertos

- **Regla ambiental resuelta por decisión del usuario:** FR-018/019 ahora distinguen procesos
  medidos, estimados y simulados. Estimados pueden conservar trazabilidad y salida estimada,
  pero verify rechaza confirmación y reportes no los acreditan. Se probaron 3 fallos iniciales
  de 6 casos nuevos antes del arreglo; después todos pasan. No se regularizan datos históricos.
- **Gráficos:** constitución §2 pide elegir una biblioteca; research.md, T035 y código usan SVG
  nativo. La justificación de simplicidad no equivale a una enmienda aprobada. Requiere decisión
  humana sobre alineación documental/técnica; no se añadió una dependencia durante la auditoría.
  Propuesta mínima en docs/entrega/ENMIENDA_CONSTITUCION_SVG.md: 1.0.0 → 1.1.0, pendiente de ratificación.
- **Paginación:** FR-008 exige listar/filtrar, pero no exige páginas. El contrato vigente declara
  arrays. No es una funcionalidad obligatoria omitida de spec.md; sí es una desviación técnica
  respecto al contrato inicial, documentada. Las listas hacen consultas por registro; el objetivo
  del plan de consultas p95 ≤2 s a 10 000 registros no está comprobado para todos los listados.
  La medición aprobada cubre panel y CSV, no permite declarar rendimiento global.
- Plan y cabecera de spec.md conciliados: main es la base, feat/001-ecogest-mvp la implementación.
  El plan conserva el diseño original con sección de equivalencias y estado posterior;
  no se reescribió en bloque ni se presentó el diseño histórico como ejecución.
- `Row = Record<string, any>` limita la comprobación estática del dominio; tsc pasa, pero no es
  garantía de tipos exhaustivos. Algunas rutas y archivos difieren del plan, con equivalencias
  registradas en tasks.md. No hay módulos fuera de alcance como IA o gestión de cultivos.
- No se certifica validez documental del PDF: control de firma/tamaño/permisos, sin antivirus.
  Entorno local con DEBUG; no es configuración para despliegue público. Sin prueba de backups.
- No se repitió una instalación completa en otro equipo: migraciones de tests parten de una base
  nueva y se verificó el lockfile con npm ci --dry-run --ignore-scripts. Es evidencia parcial de
  reproducibilidad, no una instalación limpia independiente.
- Cinco tareas siguen parciales por TDD histórico, sin alterar fechas ni resultados anteriores.

## Seguridad y Git

- Inspección de los tres commits: 129 blobs únicos, comparados con secretos locales de .env y
  patrones de tokens GitHub/OpenAI y claves privadas. Sin coincidencias. Es un análisis acotado,
  no garantía universal de ausencia de todo dato sensible.
- .env, venv, node_modules, dist y media ignorados. Código, lockfiles, migraciones, documentos,
  pruebas y capturas simuladas son candidatos de publicación después de revisión. Ningún archivo
  se agregó al staging en esta auditoría.
- Sesión/CSRF y aislamiento institucional comprobados; consultor rechazado en las 17 rutas POST
  ambientales/configuración y 5 PATCH evaluadas. Admin no hereda mutaciones ambientales.
- GitHub CLI autenticado con cuenta activa Danilo2334; identidad configurada Danilo Carlosama,
  correo noreply de Danilo2334. No se cambiaron cuentas. Sin remotos configurados.
- Estado Git actualizado: `main` en `58bab1f`, implementación en `d29b01b`, base común
  `58bab1f`. Cuatro commits, dos por autor registrado; tabla y límites de atribución en
  docs/historico/PREPARACION_GITHUB.md. Confirmación individual y PRs pendientes.

## Demostración recomendada y cierre

Seguir [DEMO_ACADEMICA.md](DEMO_ACADEMICA.md) y completar docs/entrega/REGISTRO_DEMO_HUMANA.md. Antes de
entrega definitiva: ratificar enmienda SVG, ejecutar demostración humana, revisar catálogo y rubricar
criterios con responsable, contrastar PDF docente y preparar contribuciones/PRs reales solo
con autorización de publicación. No atribuir aportes a otra cuenta por cambiar autor.

Se detiene el trabajo tras entregar este informe para revisión humana.

## Cierre puntual posterior

La regla ambiental quedó aprobada y corregida; pruebas finales y comandos en docs/PRUEBAS.md.
Se preparó docs/entrega/MATRIZ_CUMPLIMIENTO_DOCENTE.md provisional con las seis evidencias locales;
no se hace pasar por rúbrica oficial. Nuevos archivos y cambios permanecen sin commit.
Constitución 1.0.0 intacta, cinco tareas TDD históricas parciales y CHK013 pendiente.

## Actualización de la fuente docente aportada por el usuario

En la conversación se confirmaron los seis títulos del PDF, página 2:
Artefactos SDD; Aplicación funcional; Calidad técnica; Trabajo colaborativo;
Pruebas y verificación; Documentación y demo. docs/entrega/MATRIZ_CUMPLIMIENTO_DOCENTE.md ya utiliza
esos títulos y sustituye la agrupación provisional. El agente no inspeccionó el PDF original,
que continúa fuera del repositorio. No se infieren porcentajes ni aprobación de la profesora.
También se registra la exigencia comunicada de su página 8: cada integrante entrega en
Campus UCC. Ambas cargas siguen pendientes, al igual que colaboración verificable y CHK013.

## Ratificación posterior y preparación de entrega

El usuario aprobó y ratificó SVG nativo como constitución 1.1.0 el 2026-11-15. La discrepancia
constitucional queda cerrada; las referencias anteriores a propuesta pendiente son históricas.
Se preservan 12/13 criterios aprobados técnicamente (CHK004 respaldado por regresiones) y
CHK013 pendiente de ejecución humana. No cambian las cinco tareas TDD parciales.
El cierre quedó registrado en `d29b01b`, atribuido a Francisco según aclaración del usuario.
docs/historico/PREPARACION_GITHUB.md refleja el historial actual y las revisiones todavía pendientes.

Los recuentos de tres commits y estados sin commit anteriores describen etapas históricas
de la auditoría; el estado actual es el indicado en docs/historico/PREPARACION_GITHUB.md.

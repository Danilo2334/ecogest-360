# Tasks: EcoGest 360 MVP

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/api.md, quickstart.md.
**Estado**: tareas previstas, ninguna ejecutada. No iniciar hasta revisión del usuario.
**Tests**: obligatorios por solicitud; escribir y observar fallos antes de implementar cada historia.

## Phase 1: Setup

Requiere aprobación final; verificar entorno y preparar reproducibilidad, sin modificar instalaciones globales.

- [ ] T001 Revisar Python 3.12, Node compatible con Vite y PostgreSQL; registrar versiones y faltantes en docs/DECISIONES.md.
- [ ] T002 Preparar backend/manage.py, backend/config/settings.py, backend/requirements.txt y .env.example con Django 5.2 LTS, DRF y PostgreSQL; fijar dependencias sin secretos.
- [ ] T003 Preparar frontend/package.json, frontend/package-lock.json, frontend/vite.config.ts y frontend/tsconfig.json con React, TypeScript, CSS Modules, proxy y scripts typecheck/test/build/test:e2e.

## Phase 2: Foundational

Depende de T001–T003. No iniciar historias sin conexión y base de seguridad.

- [ ] T004 Definir auditoría, recibos y migraciones en backend/core/models.py y backend/core/migrations/: «Unicidad institución+actor+tipo+clave», «Inmutable; no almacenar secretos», «1–2000 caracteres» para motivos; probar rollback.
- [ ] T005 Implementar sesiones CSRF, authenticate_header para 401, permisos y errores 400/401/403/404/409 en backend/core/auth.py, backend/core/permissions.py y backend/core/errors.py.
- [ ] T006 Implementar recibos idempotentes y manejo de carreras tras rollback en backend/core/idempotency.py; pruebas de misma clave/contenido distinto en backend/tests/test_idempotency.py.
- [ ] T007 Crear cliente CSRF, manejo de error/red y reutilización de clave de operación en frontend/src/services/api.ts; estructura accesible y estilos base en frontend/src/app/App.tsx.

## Phase 3: US1 — Acceso y contexto (P1)

Prueba independiente: cuatro roles, catálogo y espacios preparados; acceso denegado sin datos privados.

- [ ] T008 [US1] Escribir escenarios de sesión, CSRF, roles, referencias cruzadas y catálogo especial en backend/tests/test_auth.py; ejecutar y registrar fallos antes de implementación (FR-001–005, SC-001).
- [ ] T009 [US1] Crear Institution/Site/Area/Membership y migraciones en backend/organizations/models.py y backend/organizations/migrations/: «1–150 caracteres», «Un rol por usuario e institución; administrador, gestor, operador, consultor».
- [ ] T010 [US1] Crear Material y migraciones en backend/catalog/models.py y backend/catalog/migrations/: «Categoría: blanco, verde, negro, especial; solo verde elegible; especial no registrable como ordinario».
- [ ] T011 [US1] Implementar contratos de institución, usuarios, roles, espacios y catálogo en backend/organizations/views.py y backend/catalog/views.py; auditar rol y bloquear autoelevación (FR-001–005).
- [ ] T012 [US1] Implementar login/logout, administración y navegación por rol en frontend/src/features/identity/IdentityPage.tsx y IdentityPage.module.css; pruebas de formularios en frontend/tests/identity.test.tsx.
- [ ] T013 [US1] Ejecutar recorrido institucional y anotar resultados reales en docs/PRUEBAS.md; validar 401/403/404 y cierre de sesión (SC-001).

## Phase 4: US2 — Generación (P1)

Depende de US1; prueba independiente con datos simulados recuperables y corrección sin asignación.

- [ ] T014 [US2] Escribir y ejecutar inicialmente pruebas de masas, procedencia, filtros, corrección auditada y persistencia en backend/tests/test_waste.py (FR-006–009, SC-005).
- [ ] T015 [US2] Crear Generation en backend/waste/models.py y backend/waste/migrations/: «Decimal(12,3), mayor que cero; saldo mayor o igual que cero», «Procedencia: medido, estimado, simulado; método obligatorio para medido/estimado; corrección solo sin Allocation».
- [ ] T016 [US2] Implementar alta, review, correct y filtros en backend/waste/services.py y backend/waste/views.py; bloquear generación al corregir, auditar antes/después y rechazar cambio de identidad (FR-006–009).
- [ ] T017 [US2] Implementar formulario, detalle e historial con decimales como texto en frontend/src/features/waste/WastePage.tsx y WastePage.module.css; pruebas de errores y recuperación en frontend/tests/waste.test.tsx.
- [ ] T018 [US2] Verificar captura 25 kg simulados, corrección 25→24 sin asignación y recuperación tras nueva sesión; registrar resultados en docs/PRUEBAS.md (SC-002, SC-005).

## Phase 5: US3 — Lotes y movimientos (P1)

Depende de US2; prueba independiente con generación precargada, reintentos y consumo concurrente.

- [ ] T019 [US3] Escribir pruebas de saldo, asignación doble, QR privado, cierre e incidencias en backend/tests/test_lots.py; demostrar fallos antes de implementar (FR-010–015).
- [ ] T020 [US3] Crear Lot, Allocation, Movement, Consumption y ConsumptionSource en backend/traceability/models.py y backend/traceability/migrations/: «Estado: abierto, agotado, cerrado», «Tipo: logístico, entrega, entrada_compostaje», «Movement único; efecto inmutable»; masas Decimal(12,3)>0 y reparto sin exceso.
- [ ] T021 [US3] Implementar locks y reparto por origen, consumo/traslado sin doble conteo y cierre en backend/traceability/services.py; bloquear corrección concurrente con asignación y rollback completo (FR-010–015).
- [ ] T022 [US3] Crear Incident en backend/core/models.py y migración adicional: «Estado: pendiente; no altera entidad ni saldos»; referencia, motivo 1–2000, autor y fecha obligatorios; acceso por matriz de permisos (FR-009).
- [ ] T023 [US3] Exponer lotes, QR, movimientos, cierre e incidencias en backend/traceability/views.py y backend/core/views.py, sin DELETE ni edición genérica.
- [ ] T024 [US3] Implementar lista/detalle, QR, movimiento e incidencia en frontend/src/features/lots/LotsPage.tsx y LotsPage.module.css; pruebas de reenvío en frontend/tests/lots.test.tsx.
- [ ] T025 [US3] Ejecutar TransactionTestCase PostgreSQL con conexiones independientes en backend/tests/test_concurrency.py: dos consumos de 4 sobre 5, duplicación de clave, corrección/asignación y rollback tras fallo; documentar en docs/PRUEBAS.md (SC-003).

## Phase 6: US4 — Compostaje verificado (P2)

Depende de US3; prueba independiente con lotes simulados, salida y evidencia privada.

- [ ] T026 [US4] Escribir pruebas de elegibilidad, estado, masa independiente, evidencia incompleta, roles y doble validación en backend/tests/test_compost.py (FR-016–019, SC-007).
- [ ] T027 [US4] Crear Process/Input/Measurement/Output y migraciones en backend/compost/models.py y backend/compost/migrations/: «Estado: en_proceso, finalizado», «Consumption único, misma institución y procedencia, material orgánico», «Un resultado consolidado por proceso»; masas Decimal(12,3)>0, unidad/fecha/tipo/autor en mediciones.
- [ ] T028 [US4] Crear Evidence/Verification en backend/compost/models.py y migraciones: «Archivo o referencia verificable obligatorio; PDF/JPEG/PNG hasta 10 MiB», «Confirmación única por proceso; rechazos históricos conservados»; receptor/fecha/descripción/autor y motivos obligatorios.
- [ ] T029 [US4] Implementar entrada atómica, finalización inmutable, evidencia privada y validación de gestor en backend/compost/services.py y backend/compost/views.py; orden proceso→generación→lote y no editar evidencia confirmada.
- [ ] T030 [US4] Implementar controles, salida, evidencia, rechazo/validación y estados separados en frontend/src/features/compost/CompostPage.tsx y CompostPage.module.css; pruebas en frontend/tests/compost.test.tsx.
- [ ] T031 [US4] Ampliar backend/tests/test_concurrency.py con entrada/finalización y doble validación; ejecutar recorrido 20→8 simulado pendiente/confirmado y privacidad de archivo, registrar en docs/PRUEBAS.md.

## Phase 7: US5 — Indicadores y CSV (P2)

Depende de US4; conjunto conocido con varias cohortes y procedencias, prueba independiente de agregaciones.

- [ ] T032 [US5] Escribir pruebas de cohortes mixtas, corte, cero, corrección vigente y CSV seguro en backend/tests/test_reports.py (FR-020–024, SC-004).
- [ ] T033 [US5] Implementar G/A/pendientes, disponible y en proceso desde agregaciones independientes en backend/reports/selectors.py; A solo ConsumptionSource de procesos verificados, nunca salida; fórmulas y límites explícitos.
- [ ] T034 [US5] Implementar dashboard y exportación filtrada con escape/neutralización y contexto en backend/reports/views.py y backend/reports/csv_export.py; mismas autorizaciones y filtros que detalle.
- [ ] T035 [US5] Implementar gráficos SVG accesibles, tabla, filtros, indicadores y descarga en frontend/src/features/reports/ReportsPage.tsx y ReportsPage.module.css; pruebas de vacío/error en frontend/tests/reports.test.tsx.
- [ ] T036 [US5] Ejecutar casos A=0/20, G=25, tasa 80 %, pendiente=5, nunca A=28; filtros medidos y CSV contra cálculo independiente; registrar evidencia en docs/PRUEBAS.md (SC-002, SC-004, SC-007).

## Phase 8: Polish & Cross-Cutting Concerns

Depende de todas las historias; no sustituye pruebas previas ni autoriza publicación.

- [ ] T037 Crear seed_demo idempotente en backend/core/management/commands/seed_demo.py con procedencia simulada y contraseñas locales no versionadas; ejecutar solo en entorno demo documentado.
- [ ] T038 Implementar y ejecutar flujo completo, teclado, foco, errores y anchuras 360/1280 en frontend/tests/e2e/vertical.spec.ts (FR-025, SC-006).
- [ ] T039 Ejecutar acceso cruzado a lista/detalle/QR/evidencia/CSV, referencias manipuladas y CSRF en backend/tests/test_security.py; asegurar admin sin mutaciones ambientales genéricas.
- [ ] T040 Ejecutar arranque limpio, migraciones reproducibles, persistencia tras reinicio y detección de modelos sin migración en backend/tests/test_persistence.py; actualizar README.md y docs/PRUEBAS.md con comandos reales.
- [ ] T041 Medir metas técnicas de panel y exportación con conjunto simulado en backend/tests/test_report_performance.py, documentando equipo, carga y resultados en docs/PRUEBAS.md; no inventar cumplimiento.
- [ ] T042 Revisar coherencia final, documentación y brechas en docs/DECISIONES.md y docs/PRUEBAS.md; solicitar revisión de entrega sin commits, push ni atribuciones no autorizadas.

## Dependencies & Execution Order

Setup → Foundational → US1 → US2 → US3 → US4 → US5 → cierre.
Dentro de historia: pruebas → modelos/migraciones → servicios → contratos → UI → validación.
Las pruebas independientes pueden usar fixtures explícitos; no implican independencia de código
entre historias. No iniciar UI integrada antes de que existan contratos implementados.

## Parallel Opportunities

No se marcan tareas completas [P]: varias agrupan integración y validación secuencial.
Ejemplos de subtareas paralelas, después de fijar contrato y modelos de su historia:
US1: preparar vistas UI y casos de permisos; US2: formulario y casos de corrección;
US3: QR UI y pruebas de carrera; US4: formulario de evidencia y pruebas de validación;
US5: tabla accesible y casos de CSV. No editar archivos compartidos simultáneamente.
No asignar autores a estas tareas; los colaboradores reales decidirán responsabilidades.

## Implementation Strategy

Primer incremento demostrable: US1 + US2, autenticación y generación recuperable.
MVP completo: todas las historias, incluido compostaje verificado y CSV. No reducirlo a login.
Priorizar un recorrido real antes de pulir pantallas. Registrar evidencia por hito y conservar
pendientes honestos. Preparar commit documental y ramas solo tras autorización explícita.


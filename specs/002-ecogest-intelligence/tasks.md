# Tasks: EcoGest Intelligence V2

Orden final recibida: T012–T025 autorizadas localmente; CHK013 humana y activación pagada de IA siguen pendientes.

## Phase 1 — Setup Brownfield

- [X] T001 Incorporar aprobación y contratos en specs/002-ecogest-intelligence/spec.md y plan.md (FR-001–028).
- [X] T002 Ejecutar línea base backend/tests y frontend/tests; registrar en docs/PRUEBAS.md (FR-001, SC-001).

## Phase 2 — Foundational

- [X] T003 Definir contrato aditivo en specs/002-ecogest-intelligence/contracts/api.md y analizar cobertura (FR-001–003,028).

## Phase 3 — US1 / A autorizada

- [X] T004 [US1] Escribir pruebas de comparación, procedencia, aislamiento y corte en backend/tests/test_observatory.py; registrar fallo antes de implementar (FR-003–008,028).
- [X] T005 [US1] Crear backend/reports/observatory.py y conectar GET en backend/core/views.py sin modificar report V1 (FR-003–008, SC-002).
- [X] T006 [US1] Definir tipos y pruebas de estados/datos en frontend/src/features/reports/types.ts y frontend/tests/observatory.test.tsx (FR-026–028).
- [X] T007 [US1] Implementar sistema visual y navegación en frontend/src/app/App.tsx, App.module.css y global.css (FR-002,026–027).
- [X] T008 [US1] Implementar frontend/src/components/MetricCard.tsx y frontend/src/features/reports/ReportsPage.tsx con gráficas, hallazgos y fuente (FR-003–008).
- [X] T009 [US1] Añadir pruebas de roles/filtros/responsive y capturas en frontend/tests/e2e/observatory.spec.ts; adaptar etiquetas de vertical.spec.ts preservando escenarios (FR-001,026–028, SC-007).
- [X] T010 [US1] Ejecutar regresión, TypeScript/build y pruebas de rendimiento de backend/tests/test_observatory.py (SC-001,002,008).
- [X] T011 [US1] Registrar evidencia y revisión de fase A en docs/PRUEBAS.md y docs/evidencias/v2/; detenerse para revisión (FR-001, SC-007).

## Phase 4 — US2 / B autorizada localmente

- [X] T012 [US2] Probar cronología, permisos, relaciones múltiples y QR anterior en backend/tests/test_passport.py (FR-009–011, SC-003).
- [X] T013 [US2] Implementar proyección en backend/traceability/passport.py con campos persistidos y ausencias explícitas (FR-009–011).
- [X] T014 [US2] Implementar frontend/src/features/lots/PassportPage.tsx y pruebas UI de ramas, saldos y evidencia (FR-009–011,026–028).

## Phase 5 — US3 / C autorizada localmente

- [X] T015 [US3] Probar x=E, x>E, G'=0, procedencia estimada y cero escritura en backend/tests/test_scenarios.py (FR-012–016, SC-004).
- [X] T016 [US3] Implementar backend/reports/scenarios.py con E/N por origen y base actual revalidada (FR-012–016).
- [X] T017 [US3] Implementar frontend/src/features/scenarios/ScenarioPage.tsx y cálculo efímero etiquetado (FR-012–016,026–027).

## Phase 6 — US4 / D autorizada localmente

- [X] T018 [US4] Probar roles, concurrencia, base congelada y evaluación en backend/tests/test_interventions.py (FR-017–020, SC-005).
- [X] T019 [US4] Crear backend/interventions/models.py y migraciones aditivas: textos 1–2000, institución compartida, estados y versión entera según data-model.md (FR-017–020).
- [X] T020 [US4] Crear backend/interventions/services.py y frontend/src/features/plans/PlansPage.tsx con auditoría, metas y comparación válida (FR-017–020,026–028).

## Phase 7 — US5 / E autorizada localmente

- [ ] T021 [US5] Aprobar modelo, presupuesto y política de datos en specs/002-ecogest-intelligence/research.md antes de habilitar red (FR-025).
- [X] T022 [US5] Probar proveedor falso, inyección, timeout, cuota, fuentes y aislamiento en backend/tests/test_intelligence.py (FR-021–025,028, SC-006).
- [X] T023 [US5] Implementar backend/intelligence/provider.py y services.py con reserva atómica, contexto mínimo y ausencia de escritura (FR-021–025).
- [X] T024 [US5] Implementar frontend/src/features/assistant/AssistantPage.tsx con tres modos, fuentes y degradación honesta (FR-021–028).

## Final Phase — Convergencia autorizada localmente

- [ ] T025 Ejecutar suite integrada, pruebas humanas y actualizar README.md y docs/PRUEBAS.md con resultados reales V2 (SC-001–008).

## Dependencies & Execution Order

T001→T002→T003→T004→T005; T006→T007→T008→T009→T010→T011→STOP.
B autorizada por orden final; C depende del contexto US1; D depende del contexto US1/C;
E requiere US1, política Q3 y presupuesto; F depende de B–E. Pruebas antes de implementación.

## Parallel Opportunities

Después de contrato, pruebas de backend y diseño CSS pueden prepararse en archivos distintos;
no ejecutar suites que comparten base de pruebas en paralelo. En B–E, pruebas API y UI separadas.

## Implementation Strategy

Incrementos verificables, no pantallas vacías de módulos futuros. Preservar ramas/main/PR.
Commits locales auténticos autorizados; push no autorizado. A no requiere esquema ni IA. Evidencia TDD V1 no se reescribe.

## Refinamiento A — aprobado 2026-11-16

- [X] T026 Actualizar FR-029–032 y SC-009–010 antes de cambios funcionales; conservar capturas originales.
- [X] T027 Documentar y probar seed_observatory_demo antes de ejecutarlo; escenario aislado, bloqueo, atomicidad, colisiones y repetición sin escritura.
- [X] T028 Refinar balance, materiales, hallazgos, acceso a cohorte, fechas y filtros móviles.
- [X] T029 Ejecutar backend 43, frontend 9, Playwright 5, TypeScript/build y capturas en cuatro anchos; comprobación representativa de contraste y teclado.
- [X] T030 Registrar docs/historico/INFORME_REFINAMIENTO_OBSERVATORIO.md y detenerse para revisión. CHK013 y TDD histórico permanecen pendientes/parciales.

Estado final T017: cálculo, UX, pruebas y transferencia revisable al plan completos. T025 conserva prueba humana pendiente.

T017: transferencia escenario→plan validada por servidor y Playwright. T018: roles, auditoría, versión obsoleta, idempotencia y ensayo concurrente real PostgreSQL aprobados.

## Phase 8: Convergence

- [X] T031 Completar restablecimiento explícito de filtros y verificar rutas con contexto en frontend/src/app/App.tsx y frontend/tests/e2e/assistant.spec.ts según FR-002/003/026 (partial, MEDIUM).
- [X] T032 Actualizar estado vigente de plan.md, data-model.md, README.md, docs/diseno/DISENO_EXPERIENCIA_V2.md y reutilizar docs/entrega/DEMO_ACADEMICA.md para recorrido V2 de 10–15 minutos; conservar historia y mapa documental según plan F (partial, MEDIUM).
- [X] T033 Ejecutar regresión integrada, capturas de cuatro anchos, teclado y revisión visual B–E; registrar resultados finales y límites en docs/PRUEBAS.md según SC-001/006/007/008/010 (partial, HIGH).

Convergencia 2026-11-16: 32 FR, 10 SC y 5 historias examinadas. Sin conflicto constitucional crítico detectado. T021 (presupuesto/prueba real IA) y T025 (componente humano SC-007/CHK013) permanecen pendientes; no se duplican ni se cierran mediante automatización.


Cierre local: T031–033 resueltas; enlaces, capturas y resultados en PRUEBAS.md. T025 parcialmente
satisfecha técnicamente, sin marcar completada por faltar ejecución humana. T021: SDK/modelo,
política y controles implementados; falta presupuesto autorizado y llamada real. No se
considera un impedimento para el modo local autorizado por la orden final.

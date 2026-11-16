# Specification Quality Checklist: EcoGest 360 Intelligence V2

**Purpose**: Revisar calidad documental antes de aprobar alcance.
**Feature**: [spec.md](../spec.md)
**Estado**: revisión documental, no prueba de software; Q1–Q3 aprobadas el 2026-11-16.

## Content Quality

- [x] Sin detalles de implementación dentro de requisitos funcionales; estrategia técnica separada.
- [x] Enfocada en valor y necesidades de usuarios institucionales.
- [x] Escrita para revisión de producto, con unidades y términos ambientales definidos.
- [x] Secciones obligatorias de plantilla completadas.

## Requirement Completeness

- [x] Q1–Q3 incorporadas conforme a aprobación explícita del 2026-11-16.
- [x] Políticas de comparación, escenarios y permisos aclaradas; presupuesto bloquea activación IA posterior.
- [x] Criterios de éxito medibles y distinguibles de resultados ejecutados.
- [x] Criterios centrados en resultados de usuario, sin imponer framework en spec.
- [x] Cinco historias con prueba independiente y escenarios de aceptación.
- [x] Casos límite: cero, ausencia de datos, filtros, concurrencia, datos ajenos y proveedor inválido.
- [x] Alcance acotado y Non-Goals explícitos.
- [x] Dependencias/supuestos y decisiones propuestas identificados.

## Feature Readiness

- [x] Todos los FR tienen cobertura en historias y SC según matriz inferior.
- [x] Flujos principales cubiertos por US1–US5 y wireframes desktop/móvil.
- [x] Resultados medibles definidos; ejecución se registra en tareas/pruebas, no en esta lista de calidad.
- [x] Plan técnico separado de especificación funcional.
- [x] Dirección y políticas aprobadas; implementación limitada explícitamente a fase A.

## Trazabilidad documental

| Requisitos | Historia / resultado | Diseño y prueba propuesta |
| --- | --- | --- |
| FR-001–003 | Todas / SC-001,007 | Navegación, contexto y regresión V1 |
| FR-004–008 | US1 / SC-002,008 | Observatorio, comparación, ranking y hallazgos |
| FR-009–011 | US2 / SC-003 | Pasaporte, ramas y QR privado |
| FR-012–016 | US3 / SC-004 | Base/escenario, límites y no escritura |
| FR-017–020 | US4 / SC-005 | Planes, evaluación y matriz de roles |
| FR-021–025 | US5 / SC-006,008 | Modos, evidencia, fallos y política de coste |
| FR-026–028 | Todas / SC-003,006,007 | Estados, accesibilidad y privacidad |

## Notas de revisión

La plantilla activa se resolvió mediante `specify preset resolve spec-template`; archivo core
.specify/templates/spec-template.md. Numeración secuencial 002 y selector feature.json actualizado.
No existe .specify/extensions.yml: no hay hooks before/after_specify registrados que ejecutar.
No se ejecutaron workflows plan/tasks: el brief establece aprobación previa de spec y UX.
Las 38 pruebas previas siguen siendo evidencia V1; CHK013 y cinco tareas TDD conservan su estado.
La revisión cruza brief, constitución, spec y UX; no sustituye speckit-analyze sobre plan/tasks futuros.

Actualización: plan/tareas autorizados el 2026-11-16. Notas previas describen el estado anterior.

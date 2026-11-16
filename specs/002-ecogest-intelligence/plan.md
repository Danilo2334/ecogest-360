# Implementation Plan: EcoGest 360 Intelligence V2

**Branch**: feat/002-ecogest-intelligence | **Date**: 2026-11-16 | **Spec**: [spec.md](spec.md)

## Summary

Evolución aditiva del MVP. Fase A autorizada: Observatorio de lectura y sistema visual sin
cambiar fórmulas V1, modelos ni datos. Fases B–F solo planificadas y requieren nueva autorización.

## Technical Context

Python 3.12, Django 5.2/DRF, PostgreSQL 16; React/TypeScript/Vite y CSS Modules existentes.
Sin dependencias nuevas ni migraciones en A. SDK OpenAI solo en fase E posterior y con presupuesto.
Pruebas Django/PostgreSQL, Vitest, Playwright. Windows local, responsive 360/390/768/1280.
Objetivo SC-008: p95 ≤2 s, 10 000 registros/10 lectores, 100 muestras. Sin promesa de producción.

## Constitution Check

Antes/después de diseño: conforme. Cantidades/locks/idempotencia V1 intactos, lectura institucional,
procedencias separadas, sin datos inventados, QR privado y sin IA obligatoria. Sin enmiendas.
Reglas ambientales conservadas. Las capturas serán de ejecución real con procedencia visible.

## Project Structure

A: backend/reports/observatory.py, backend/core/views.py (GET nuevo), backend/tests/test_observatory.py;
frontend/src/features/reports/{ReportsPage.tsx,Observatory.module.css,types.ts};
frontend/src/components/MetricCard.tsx; frontend/src/app/{App.tsx,App.module.css,global.css};
frontend/tests/observatory.test.tsx y frontend/tests/e2e/observatory.spec.ts.
B futura: backend/traceability/passport.py, frontend/src/features/lots/PassportPage.tsx.
C futura: backend/reports/scenarios.py, frontend/src/features/scenarios/ScenarioPage.tsx.
D futura: backend/interventions/{models,services,views}.py y migraciones, frontend/src/features/plans/.
E futura: backend/intelligence/{provider,context,services,views}.py, frontend/src/features/assistant/.
F: docs/PRUEBAS.md, docs/evidencias/v2/, README.md.

## Arquitectura y secuencia

Componer report() V1 sin modificarlo: un cutoff común para actual/anterior; agregar series por día,
ranking por ID de área y hallazgos deterministas; endpoint GET /api/observatory nuevo y autorizado.
Sin fechas válidas o procedencia única, respuesta explica comparación deshabilitada.
El frontend reutiliza sesión, filtros y formularios; nuevo componente analítico tipado.
Nombres de navegación Observatorio/Trazabilidad; enlaces UUID anteriores conservados.
Menú móvil desplegable por botón, sin ocultar acceso a formularios existentes. Sin enlaces muertos
hacia funcionalidades futuras. Contexto limpiado al logout y datos obsoletos retirados al recargar.

Fases: setup/regresión → pruebas nuevas fallidas → A backend → A interfaz → regresión/capturas → STOP.
Después de nueva autorización: B pasaporte → C escenarios → D planes → E IA → F convergencia.
Pasaporte/escenarios no requieren modificar entidades V1; planes y cuotas futuras sí adiciones.

## Complexity Tracking

No excepciones constitucionales ni nuevas bibliotecas. No rehacer dispatch ni report V1.
Ver research.md, data-model.md, contracts/api.md y quickstart.md para contratos verificables.
# Adenda de refinamiento A — 2026-11-16

FR-029–032 / SC-009–010: comando explícito seed_observatory_demo sobre modelos existentes,
transacción PostgreSQL y bloqueo asesor; manifiesto AuditEvent y huella de registros con institución.
Sin migraciones. Cohorte sintética separada, servicios de dominio V1 para saldos/compostaje.
Balance SVG/CSS y barras se basan en summary existente; extensión aditiva de insights con
interpretation/suggestion/area. Sin dependencias nuevas ni llamadas externas.
Controles nativos conservados; resumen es-CO elimina ambigüedad aun si el navegador dibuja MM/DD.
Pruebas del generador preceden implementación y ejecución; pruebas UI adicionales verifican
cohorte y filtros. Pasaporte/Simulador/Planes/IA no forman parte de este incremento.


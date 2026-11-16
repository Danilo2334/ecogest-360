# Implementation Plan: EcoGest 360 MVP

**Branch**: implementación en `feat/001-ecogest-mvp`; base `main` (rama usada al preparar el diseño).
**Date**: 2026-11-15 | **Spec**: [spec.md](spec.md)
**Input**: Especificación aclarada Q1 B, Q2 A, Q3 A y cierre CHK004 aprobado.
**Estado**: diseño original conservado con conciliación posterior; implementación y auditoría locales ejecutadas.

## Summary

Aplicación modular con sesión institucional y flujo vertical generación → lote → movimiento →
compostaje → validación → indicadores. Operador confirma operaciones ordinarias; gestor acredita
resultados. Consumos transaccionales, trazabilidad por origen e idempotencia evitan sobreconsumo.
Conservar generación independiente de movimiento y de salida de compost.

## Technical Context

**Language/Version**: Python 3.12; TypeScript, React y Vite con versiones compatibles fijadas al implementar.
**Primary Dependencies**: Django 5.2 LTS, DRF, psycopg, generador QR; CSS Modules sin framework CSS adicional.
**Storage**: PostgreSQL 16 objetivo; archivos de evidencia privados locales. Sin SQLite como sustituto.
**Testing**: Django TestCase/APITestCase; TransactionTestCase para concurrencia real;
Vitest/Testing Library; Playwright para recorrido vertical, permisos y accesibilidad funcional.
**Target Platform**: Desarrollo Windows PowerShell; navegador móvil/escritorio. Sin despliegue público.
**Project Type**: Web, monolito modular con frontend separado durante desarrollo y mismo origen lógico.
**Performance Goals**: Meta técnica inicial, no resultado medido: panel y consultas p95 ≤2 s
con 10 000 registros y 10 usuarios locales concurrentes; CSV de 10 000 filas ≤10 s.
Medir en equipo documentado; ajustar objetivos explícitamente si el piloto requiere otra escala.
**Constraints**: No servicios pagos, LLM, sensores ni nuevos módulos. Decimales exactos, permisos
por institución, saldos y correcciones protegidos. No instalación ni migración en esta etapa.
**Scale/Scope**: Una universidad, cuatro roles, cinco historias; datos de demo simulados.

## Constitution Check

| Regla | Antes de diseño | Después de diseño / evidencia documental |
| --- | --- | --- |
| Stack y seis apartados | Conforme | Stack preservado; constitución sin cambios |
| Pesos positivos, saldo, reintentos | Conforme | Decimal, locks, recibos únicos y pruebas concurrentes |
| No doble conteo | Conforme | ConsumptionSource y agregaciones independientes |
| Medido/estimado/simulado | Conforme | Etiqueta conservada, filtros en panel/CSV |
| Mínimo privilegio y QR privado | Conforme | Matriz roles, consultas acotadas y descarga autorizada |
| Auditoría y no borrado silencioso | Conforme | Correct solo sin asignación; incidencias sin mutación histórica |
| Compostaje independiente y evidencia | Conforme | Finalización separada de verificación, A solo entradas acreditadas |
| Fuentes SDD y pruebas reales | Conforme | Contratos, guía y tareas; ejecución de software pendiente |

La conformidad es de diseño, no certifica implementación ni pruebas. No hay excepción constitucional.
Revisar la delimitación de aprovechamiento externo en spec.md antes de aprobar alcance final.

## Project Structure

### Documentation (this feature)

spec.md, plan.md, research.md, data-model.md, contracts/api.md, quickstart.md, tasks.md,
checklists/requirements.md y checklists/integridad-ambiental.md.

### Source Code (repository root)

Rutas futuras, no creadas en esta etapa:

- backend/config/: settings.py, urls.py; backend/manage.py y requirements.txt.
- backend/core/: auth.py, permissions.py, idempotency.py, errors.py, models.py, migrations/.
- backend/organizations/: models.py, serializers.py, views.py, migrations/.
- backend/catalog/: models.py, serializers.py, views.py, migrations/.
- backend/waste/: models.py, services.py, serializers.py, views.py, migrations/.
- backend/traceability/: models.py, services.py, views.py, migrations/.
- backend/compost/: models.py, services.py, views.py, migrations/.
- backend/reports/: selectors.py, views.py, csv_export.py.
- backend/tests/: test_auth.py, test_waste.py, test_lots.py, test_concurrency.py,
  test_compost.py, test_reports.py, test_security.py, test_persistence.py.
- frontend/src/: app/, services/api.ts, components/, features/{identity,waste,lots,compost,reports}/.
- frontend/tests/: formularios y e2e/vertical.spec.ts.
- docs/DECISIONES.md, docs/PRUEBAS.md, README.md, .env.example.

**Structure Decision**: Dominios pequeños, servicios explícitos para mutaciones y selectores
para reportes. No repositorios abstractos ni microservicios. Migraciones bajo cada aplicación.

## Diseño y secuencia

1. Investigación documental completada en research.md; decisiones y alternativas registradas.
2. Modelo y contratos en data-model.md y contracts/api.md; guía reproducible en quickstart.md.
3. Preparación futura: revisar entorno sin alterar globales, aprobar artefactos, preparar Git
   inicial y ramas solo cuando el usuario autorice commits. No atribuir trabajo a colaboradores.
4. Base: proyecto, conexión PostgreSQL, errores, sesiones, permisos, auditoría e idempotencia.
5. US1 y US2 completas en web: acceso y registro recuperable antes de añadir procesos.
6. US3: lotes, reparto por origen, consumo, QR, concurrencia e incidencias.
7. US4: entradas, salida independiente, evidencia privada y validación única del gestor.
8. US5: agregaciones sin duplicación, filtros por cohorte/corte, CSV y accesibilidad.
9. Arranque limpio, persistencia, migraciones, demo, documentación y evidencia real.

## Integridad y seguridad

Toda mutación se ejecuta en atomic; bloqueos proceso → generación → lote y UUID ascendente
cuando hay varios objetos. Corrección y asignación compiten sobre Generation. La confirmación
bloquea Process y sus evidencias son inmutables después; hay una sola confirmación exitosa.
Idempotencia debe comprobarse antes de volver a validar un estado que cambió por el primer envío.
Las restricciones únicas resuelven carreras; una excepción de integridad obliga a rollback.
No confiar en filtros UI: queryset institucional y autorización de acción siempre en servidor.
CSRF en login y mutaciones, sesión HttpOnly, 401 adaptado y 403 permisos, 404 no visible.
Adjuntos por tipo real y tamaño, rutas no controladas por usuario, descarga autenticada.
No ofrecer endpoint de DELETE ambiental ni edición genérica de modelos sensibles en admin.

## Pruebas y puertas de calidad

Cada historia tiene tests de contrato/dominio antes de cerrar su implementación y recorrido UI.
PostgreSQL es obligatorio para saldo concurrente, recibos duplicados, corrección/asignación y
entrada/finalización. Inyectar fallo después de crear movimiento y comprobar rollback completo.
Validar A con orígenes de diferentes cohortes/áreas en un mismo proceso: solo entradas del filtro.
Comparar CSV y panel, cortar antes/después de confirmación y repetir confirmación.
Pruebas de acceso ajeno incluyen listas, detalle, QR, evidencia, reportes y referencias enviadas.
La guía distingue comandos futuros de ejecuciones. Documentar todo fallo en docs/PRUEBAS.md.
La lista de calidad personalizada permanece abierta para revisión humana; no marca trabajo hecho.

## Complexity Tracking

Sin excepciones constitucionales. Una entidad de reparto por origen y un recibo idempotente
son necesarios para cohortes e integridad, no nuevas funcionalidades de usuario.

## Conciliación posterior al diseño

Las frases «futuro», «sin migración» y «pendiente de ejecución» anteriores describen la etapa
original, no el estado actual. Resultados vigentes en docs/PRUEBAS.md y tasks.md.
Transporte REST centralizado en core/views.py; servicios siguen separados por dominio.
Movement representa el consumo, con ConsumptionSource para reparto; Incident está en migración
inicial. CSS Modules compartidos y pruebas agrupadas por riesgo/flujo sustituyen rutas previstas
sin cambiar las reglas funcionales. Listas sin paginación: desviación técnica documentada,
no requisito funcional agregado; no se ha validado rendimiento de todos los listados a escala.

CHK004: verify bloquea procesos estimados y salidas de procedencia incompatible; el selector
excluye acreditaciones estimadas históricas sin borrar su historial. No cambian esquema,
masas, locks ni idempotencia. Medidos requieren salida independiente y evidencia; simulados
mantienen etiquetas y filtros. Pruebas nuevas antes del arreglo, sin rehacer historial TDD.

SVG nativo se conserva en código y queda permitido por constitución 1.1.0, ratificada
el 2026-11-15. docs/ENMIENDA_CONSTITUCION_SVG.md registra la aprobación. La discrepancia
detectada en auditoría queda cerrada, sin cambiar dominio ni añadir dependencias.

# Cambios locales preparados para revisión

La auditoría se realizó inicialmente sin commits. El usuario autoriza ahora reunir los
cambios revisados en un commit local de cierre, conservando los tres commits históricos.
Rama: feat/001-ecogest-mvp; base: main. Historial preservado:

| Commit | Contenido | Autor real |
| --- | --- | --- |
| 58bab1f | Documentación SDD inicial | Danilo Carlosama / Danilo2334 |
| fd90a7d | API PostgreSQL y pruebas | Danilo Carlosama / Danilo2334 |
| 86fac23 | Flujo web y documentación del MVP | Danilo Carlosama / Danilo2334 |

## Agrupación sugerida, sin ejecutar commits

1. Correcciones de auditoría: core/validation.py, core/views.py, validación de evidencia en
   compost/services.py; fecha local en shared.tsx; regresiones test_audit.py/date.test.tsx;
   sincronización de logout en Playwright y zona de navegador. No atribuirlas a Francisco.
2. Cierre CHK004: regla y aceptación en spec.md, restricciones en compost/services.py,
   reportes en reports/selectors.py, presentación CompostPage.tsx, regresiones de procedencia
   y formulario; contrato actualizado. Panel/CSV no acreditan estimados; medidos y simulados
   conservan procedencia. Ningún cambio requiere migración ni modificación de datos previos.
3. Evidencia documental: auditoría, PRUEBAS, DECISIONES, conciliación del plan/README/checklist,
   guion y hoja humana vacía, matriz docente provisional, propuesta SVG y capturas simuladas.
   La propuesta no equivale a ratificación; las cinco tareas TDD históricas no se cierran.

Hay archivos compartidos entre grupos: revisar diff y seleccionar cambios coherentes antes de
un eventual commit. Este documento no autoriza publicar ni dividir artificialmente autorías.

Excluir siempre .env, contraseñas, venv, node_modules, dist, media y resultados temporales.
Incluir solo código, tests, documentos y capturas revisados sin datos sensibles.
Constitución 1.0.0 y tres commits intactos. Sin remoto ni PRs; la colaboración de Francisco
requiere un aporte real realizado/verificado por él, con autorización posterior de publicación.

## Actualización tras aprobación explícita de SVG

La enmienda ya está ratificada: constitución vigente 1.1.0, fecha 2026-11-15. Las menciones
anteriores a propuesta describen el estado previo. Incluir el cambio constitucional mínimo
y retirar su comentario temporal de revisión antes del futuro commit, sin alterar las reglas.
Propuesta concreta y comandos futuros: PREPARACION_GITHUB.md; texto de PR: PR_MVP_PROPUESTO.md.
Commit sugerido: `fix: cerrar auditoria ambiental y ratificar constitucion 1.1.0`.
No ejecutado; autor real Danilo, sin reatribuir historial ni contribución de Francisco.

## Autorización posterior de cierre local

El commit de cierre queda autorizado con identidad verificada de Danilo. Los apartados
anteriores describen su preparación histórica; el hash y manifiesto definitivo se obtienen
con `git log -1 --format=fuller` y `git show --name-status HEAD` después de crearlo.
Incluye correcciones ya probadas, constitución 1.1.0, regresiones, documentación y cuatro
capturas simuladas. No incluye .env, media, dependencias instaladas ni datos de desarrollo.
Sin acciones remotas. CHK013 y T008/T014/T019/T026/T032 no cambian de estado.

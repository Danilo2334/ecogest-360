# Refinamiento del Observatorio — 2026-11-16

Implementado únicamente en feat/002-ecogest-intelligence. Dirección visual conservada;
revisión humana de este refinamiento pendiente. Pasaporte, Simulador, Planes e IA no implementados.

## Resultado funcional

- Evolución diaria con comparación, tabla de valores y huecos honestos.
- Balance visual G = A + pendiente; salida de compost no se suma. Distribución por materiales.
- Hallazgos con observación, magnitud, interpretación limitada y recomendación desplegable;
  mayor área informa que masa absoluta no equivale a eficiencia.
- KPI llevan a la cohorte base; hallazgo de área conserva fechas, procedencia, material y corte.
  Consultar cohorte no implica que todos sus registros estén acreditados.
- Filtros plegables en móvil/tablet; período siempre visible. Hallazgos antes de la evolución
  en vista estrecha. Texto y objetivos de interacción ampliados.
- Fechas descriptivas es-CO; controles nativos conservados. Chromium de esta máquina sigue
  dibujando MM/DD/YYYY dentro del control, aunque lang/locale sea es-CO. El resumen escrito en
  español muestra el período sin ambigüedad; no se sustituyó por un campo de texto frágil.

## Datos demostrativos

Ver [mecanismo, fórmula y ejecución](../evidencias/DATOS_DEMO_OBSERVATORIO.md).
Generador documentado y probado antes de ejecutar en la base local. Creó 84 generaciones,
tres áreas, tres materiales y dos procesos en otra institución. Repetición local con --apply
devolvió el mismo manifiesto/huella sin agregar datos. No se restablecieron cuentas anteriores.
Los escenarios ambientales y las validaciones son SIMULADOS y ejecutados por el comando,
no por un humano; las fechas reales de creación no se reescriben.

Para revisar en http://127.0.0.1:5178/: cuenta `intelligence_gestor`, contraseña DEMO_PASSWORD
del .env local (misma inicial de demo, no se imprime). Procedencia Simulado; Desde 2026-11-02,
Hasta 2026-11-15, sin área/material/corte. La cuenta demo_gestor sigue en la institución anterior.

| Resultado del escenario | Valor |
|---|---:|
| Generación actual / anterior | 365 / 281 kg |
| Diferencia | +84 kg / +29,89 % |
| Entrada acreditada actual | 100 kg |
| Pendiente actual | 265 kg |
| Tasa actual | 27,40 % |
| Cafetería / Aulas / Oficinas | 187 / 103 / 75 kg |

El propósito es explorar registros sintéticos, no afirmar una mejora ambiental real.

## Verificación ejecutada

| Comprobación | Resultado |
|---|---|
| Primer test del generador, antes del comando | 4 casos: 3 errores por comando inexistente, 1 pasó al esperar CommandError; no se afirma que los cuatro fallaran |
| Generador implementado, base de pruebas | 4/4; dry-run, repetición/aislamiento/cifras, colisión de usuario, cambio posterior sin reparación |
| Suite backend completa | 43/43, 76,059 s |
| Vitest completa, tras últimos cambios UI | 9/9 |
| TypeScript + build final | Correctos; JS 258,20 kB / gzip 79,59 kB |
| Playwright completo | 5/5, 19,5 s; conserva tres recorridos MVP y roles del Observatorio |
| Refinamiento con contraste/teclado añadido | 1/1, 3,4 s; mínimo 5,43:1 entre cinco textos representativos |
| Responsive | 360, 390, 768 y 1280 sin scroll horizontal de página; capturas reales inspeccionadas |
| Rendimiento Observatorio | 10 000 registros, 10 lectores, 100 consultas; p95 0,418 s |
| Rendimiento V1 / CSV | p95 conservador 0,073 s / CSV 0,598 s |
| Migraciones pendientes | Ninguna: makemigrations --check --dry-run |
| git diff --check | Correcto; advertencias de conversión LF/CRLF |

Se comprobó teclado en menú, acción de KPI y desplegable de interpretación; filtros conservados,
14 filas temporales y balance 365=100+265. Las pruebas existentes cubren permisos, masas,
duplicación, procedencias y cortes. Cinco muestras de contraste no equivalen a auditoría WCAG
completa. CHK013 no está ejecutada; las cinco tareas TDD históricas siguen parciales.
Los nuevos tests UI se añadieron durante el refinamiento: no se inventa una fase roja previa.

Defectos corregidos durante validación: selector de prueba de Área demasiado estricto (cambiado
a combobox y opción seleccionada); espacio vacío por altura de hallazgos (balance integrado
bajo evolución); filtros móviles extensos (plegables). El primer recorrido nuevo falló por el
selector; después pasó individualmente y en la suite completa.

## Capturas reales antes y después

Las anteriores corresponden a la cohorte original; las posteriores a la nueva cohorte SIMULADA.
La diferencia de cifras no es resultado de una intervención ambiental ni comparación experimental
del mismo universo. Las capturas originales se copiaron antes de regenerar evidencias.

| Ancho | Antes | Después |
|---|---|---|
| 1280 | [Captura](../evidencias/v2/antes-refinamiento/observatorio-1280.png) | [Captura](../evidencias/v2/despues-refinamiento/observatorio-1280.png) |
| 768 | [Captura](../evidencias/v2/antes-refinamiento/observatorio-768.png) | [Captura](../evidencias/v2/despues-refinamiento/observatorio-768.png) |
| 390 | [Captura](../evidencias/v2/antes-refinamiento/observatorio-390.png) | [Captura](../evidencias/v2/despues-refinamiento/observatorio-390.png) |
| 360 | [Captura](../evidencias/v2/antes-refinamiento/observatorio-360.png) | [Captura](../evidencias/v2/despues-refinamiento/observatorio-360.png) |

## Archivos de esta intervención

Nuevos: backend/core/management/commands/seed_observatory_demo.py,
backend/tests/test_observatory_demo.py, frontend/tests/e2e/refinement.spec.ts,
docs/evidencias/DATOS_DEMO_OBSERVATORIO.md, este informe, carpetas de capturas antes/después.

Actualizados: backend/reports/observatory.py, backend/tests/test_observatory.py;
frontend/src/components/MetricCard.tsx, frontend/src/features/reports/{ReportsPage.tsx,
Observatory.module.css,types.ts}, frontend/src/app/{App.tsx,App.module.css},
frontend/index.html, frontend/playwright.config.ts, frontend/tests/observatory.test.tsx;
specs/002-ecogest-intelligence/{spec.md,plan.md,tasks.md,contracts/api.md},
docs/DECISIONES.md y docs/PRUEBAS.md. Las capturas de fase A en la raíz de evidencias/v2
también se regeneran por la prueba anterior; sus versiones previas están preservadas en antes-refinamiento.
El árbol incluye además cambios de la fase A anterior que ya estaban pendientes.

## Git y punto de parada

Rama feat/002-ecogest-intelligence; HEAD 34ce7bf24463a3ce476cdb52e9c002f2ab777faf.
main sigue en 58bab1f87373d0110b088fc5d894a9f9f467e104 y feat/001-ecogest-mvp en
34ce7bf24463a3ce476cdb52e9c002f2ab777faf. Cambios locales sin staging ni commits nuevos.
No push, merge, despliegue, cambios de autoría, constitución ni PR #1.
Se detiene aquí para revisión del Observatorio, antes del Pasaporte.

# Registro de comprobaciones

## 2026-11-15 — Documentos SDD

En este primer hito solo se realizaron verificaciones documentales. Los resultados de la
implementación posterior se registran abajo; no confundir ambos momentos.

| Procedimiento ejecutado | Resultado |
| --- | --- |
| check-prerequisites -Json -PathsOnly | Resolvió specs/001-ecogest-mvp |
| check-prerequisites -Json -Template checklist-template, antes del plan | Falló: plan.md inexistente |
| setup-plan -Json | Creó plantilla activa de plan en la feature |
| check-prerequisites -Json -Template checklist-template, después del setup | Resolvió plantilla correctamente |
| setup-tasks -Json | Resolvió plantilla y encontró investigación, modelo, contratos y guía |
| check-prerequisites -Json -RequireSpec -RequireTasks -IncludeTasks | Reconoció artefactos requeridos |
| git branch --show-current | main |

Los scripts se invocaron con powershell -NoProfile -ExecutionPolicy Bypass -File, limitado
al proceso, sin cambiar la política global. Los escenarios de software por ejecutar se
encuentran en quickstart.md y tasks.md. No confundir casillas de calidad con tests aprobados.

## 2026-11-15 — MVP implementado y ejecutado localmente

Entorno: Windows, Intel Core i5-11400H 2.70 GHz, aproximadamente 16 GiB RAM;
Python 3.12, Node 22.23.3, npm 10.9.9, Django 5.2.19, DRF 3.18.3,
PostgreSQL 16 en Docker Desktop, React y Vite 8.3.8. Versiones exactas reproducibles
en requirements.txt y package-lock.json. Sin cambios a instalaciones Python globales.

### Resultados finales ejecutados

| Comando/procedimiento | Resultado observado |
| --- | --- |
| `manage.py migrate` en base nueva ecogest | Migraciones Django y seis aplicaciones propias aplicadas |
| `manage.py check` | Sin problemas |
| `manage.py makemigrations --check --dry-run` | Sin cambios de modelos pendientes |
| `manage.py test tests --noinput` | **20 pruebas aprobadas**, 40.348 s, PostgreSQL real |
| `npm.cmd run test -- --run` | **3 pruebas aprobadas**, 2 archivos Vitest |
| `npm.cmd run typecheck` | TypeScript sin errores |
| `npm.cmd run build` | Compilación de producción correcta |
| `npm.cmd run test:e2e` | **3 recorridos aprobados**, Chromium, 11.1 s |
| `npm.cmd ci` | Instalación reproducible del lockfile completada |
| `pip check` y `npm audit` | Dependencias Python compatibles; 0 vulnerabilidades reportadas por npm en la ejecución |
| Reiniciar servidor Django y consultar registros | 1 registro antes y 1 después en ese momento; ejecuciones E2E posteriores agregan datos simulados |
| Consultar privilegios PostgreSQL de aplicación | ecogest_app: SUPERUSER=false, CREATEROLE=false |

Los comandos completos y sus directorios están en README.md. Las pruebas Django crean y
eliminan test_ecogest; los recorridos de navegador usan ecogest y conservan sus demos.
No se borraron datos para forzar totales ni se utilizaron mediciones ambientales reales.

### Cobertura comprobada

- `test_vertical.py`: 25 kg generados, 20 kg a compostaje, salida independiente de 8 kg,
  acreditación de 20 kg, pendiente 5 kg y 80 %; nunca 28 kg acreditados. Masas inválidas y lector.
- `test_security.py`: login/logout con CSRF real, cuatro roles, aislamiento en listas,
  detalle, QR, evidencia y CSV; corrección 25→24 auditada, incidencias, categoría especial,
  claves repetidas con contenido diferente y rollback con fallo inyectado.
- `test_concurrency.py`: conexiones independientes y consumos 4+4 sobre saldo 5,
  repetición simultánea de clave, corrección contra asignación, entrada contra finalización,
  doble confirmación sin duplicar efecto.
- `test_compost.py`: elegibilidad, procedencia, evidencia incompleta, permisos, corte,
  procesos cerrados, cohortes mixtas, controles y carga/descarga privada de documento.
- `test_reports.py`: entrega externa separada de acreditación, filtros inválidos,
  contexto CSV, neutralización de fórmulas y recuperación de información.
- `test_persistence.py`: recuperación tras cerrar conexión y crear cliente independiente.
- Vitest: error visible conservando masa, reintento con misma clave, nueva clave al corregir,
  éxito y limpieza de formulario; universo vacío sin tasa inventada y filtro del enlace CSV.
- Playwright: login, generación, lote, entrada y salida, evidencia, validación por gestor,
  exportación; consultor sin escritura; captura por teclado, foco y cinco pantallas a 360/1280 px.
  Sin errores JavaScript en el flujo vertical ni desbordamiento horizontal de la página.

### Rendimiento local, no garantía de producción

10 000 generaciones simuladas de 1 kg, 10 lectores concurrentes mediante APIClient y
conexiones PostgreSQL independientes. Máximo de las diez muestras (p95 conservador):
**0.072 s**, objetivo <2 s. Preparación del informe y CSV: **0.675 s**, objetivo <10 s.
CSV mide selector y serialización, sin descarga por red; panel no incluye render del navegador.
Es una muestra local pequeña, no una prueba de carga sostenida ni certificación de capacidad.

### Fallos encontrados y corregidos

- Primer flujo rojo: módulos todavía inexistentes (`No module named organizations`).
  Varias pruebas especializadas fueron posteriores al código: no existe evidencia TDD completa.
- Descubrimiento sin etiqueta desde raíz encontró 0 pruebas: se fijó el comando `test tests`.
- Primera medición de panel: 7.583 s; se sustituyó materialización de filas por agregaciones SQL.
- Selectores accesibles del navegador ambiguos: etiquetas explícitas e iconos decorativos
  fuera del nombre accesible. Recorridos finales aprobados.
- `npm ci` falló EPERM por DLL de Vite en uso: se detuvo solo el proceso propio y se reinstaló.
- Prueba de archivo cerraba conexión antes de comprobar anónimo: se corrigió orden de cierre.
- Hook beforeEach devolvía una función mock rechazada: se corrigió el hook; Vitest final aprobado.

### Límites y revisión pendiente

- 13 criterios personalizados de integridad ambiental siguen abiertos para revisión humana.
- T008/T014/T019/T026/T032 tienen cobertura funcional, pero permanece incumplida la secuencia
  histórica estricta de escribir y observar cada prueba antes del código. No se puede reconstruir
  retrospectivamente esa evidencia; no se marca esa parte como completada.
- Pruebas se agrupan por riesgo y recorrido, no en todos los nombres de archivos del plan.
  Formularios comparten ActionForm; E2E verifica integración, Vitest comportamiento compartido.
  No hay cobertura exhaustiva de todas las combinaciones de errores o navegadores.
- Listados sin paginación; archivos PDF revisados por firma y permisos, sin antivirus.
  No se realizó despliegue, prueba de recuperación de backup ni revisión WCAG formal.
- Capturas versionadas en docs/evidencias/ muestran exclusivamente demostración simulada.
  Totales dependen del número de ejecuciones previas; no constituyen mediciones reales.

## 2026-11-15 — Auditoría posterior, sin commits

Informe detallado: [AUDITORIA_FINAL.md](AUDITORIA_FINAL.md); guion humano:
[DEMO_ACADEMICA.md](DEMO_ACADEMICA.md). No se sustituyen resultados históricos.

| Ejecución en esta auditoría | Resultado |
| --- | --- |
| Suite backend original | 20/20 aprobadas, 40.435 s |
| Regresiones nuevas antes de arreglo | Evidencia null: cuatro aserciones fallidas; campo inesperado de archivo: KeyError confirmado en ejecución aislada |
| Suite backend tras correcciones | **24/24 aprobadas**, 40.522 s, PostgreSQL real |
| Panel con 10 000 generaciones y 10 lectores | Máximo de diez muestras 0.060 s; CSV 0.600 s; mismos límites metodológicos anteriores |
| Vitest original | 3/3 aprobadas |
| Regresión fecha antes de arreglo | 1 fallida: 2026-11-16 en lugar de 2026-11-15 a las 23:30 de Bogotá |
| Vitest final con TZ=America/Bogota | **4/4 aprobadas**, 3 archivos |
| TypeScript y build final | Correctos; build incluye tsc --noEmit |
| Playwright inicial | 3/3 aprobados, 11.9 s |
| Playwright ampliado con capturas | 1 fallo por carrera del test entre logout y navegación; 2 aprobados |
| Playwright tras esperar logout | 3/3 aprobados, 10.1 s; repetición tras ajuste de fecha registrada abajo |
| Playwright final con fecha local y navegador America/Bogota | **3/3 aprobados**, 10.3 s |
| Django check / makemigrations --check --dry-run | Sin problemas / sin cambios pendientes |
| showmigrations --plan | Todas las migraciones existentes aplicadas; no se ejecutaron migraciones sobre la base de desarrollo en esta auditoría |
| pip check | Sin dependencias incompatibles |
| npm ci --dry-run --ignore-scripts | Lockfile aceptado; simulación, no reinstalación completa |
| npm audit --omit=dev | 0 vulnerabilidades reportadas en dependencias de producción; no escáner de backend |
| Escaneo Git de secretos | 3 commits, 129 blobs únicos, sin coincidencias de secretos locales/patrones buscados |

Nuevas pruebas backend: test_audit.py cubre nulos en evidencia, adjunto con campo inesperado,
22 acciones denegadas al consultor, PNG QR y consulta autorizada/anonimato. Los roles restantes,
aislamiento, decimales, doble conteo, persistencia, concurrencia y CSV conservan sus suites.
La generación PNG y lookup UUID no equivalen a una decodificación óptica: cámara pendiente.

El test QR inicialmente cerraba FileResponse dentro de TestCase, cerrando su conexión antes del
siguiente fixture; se corrigió el test. Las nuevas regresiones sí tienen rojo/verde observado;
T008/T014/T019/T026/T032 permanecen parciales por falta de evidencia histórica anterior.

No se borraron registros de desarrollo. Los recorridos agregaron generaciones y comprobantes
simulados, incluidos intentos de demo incompletos del test fallido. Sus totales no deben
interpretarse como una sola cohorte de 25 kg. El guion usa un área nueva para aislar cifras.
11 criterios ambientales aprobados técnicamente; CHK004 y CHK013 pendientes según el informe.
No se adjudica aprobación humana ni cumplimiento del PDF docente no disponible localmente.

## 2026-11-15 — Cierre puntual CHK004

Se aprobaron primero FR-018/019 y cuatro criterios de aceptación en spec.md. Después se creó
test_compost_provenance.py y se ejecutó **antes de corregir el código**:
6 pruebas, **3 aprobadas y 3 fallidas** en 9.775 s. Fallos reproducidos: estimado confirmado
(201 frente a 400), salida histórica incompatible confirmada (201 frente a 400) y confirmación
estimada histórica sumada a A (20 frente a 0). No se extrapola este rojo/verde al desarrollo previo.

Corrección mínima: verify exige proceso medido/simulado y salida independiente de igual
procedencia; rechaza estimados. Selector del panel/CSV excluye confirmaciones estimadas y
salidas incompatibles. UI informa la restricción y no ofrece confirmar estimados, pero mantiene
posibilidad de rechazo y trazabilidad. No se borran evidencias ni se cambian masas/procedencias.

| Comando ejecutado desde raíz, salvo frontend | Resultado final |
| --- | --- |
| `backend/.venv/Scripts/python.exe backend/manage.py test tests --noinput` | **30/30 aprobadas**, 50.888 s, PostgreSQL real |
| `npm.cmd run test -- --run` en frontend, con TZ=America/Bogota | **5/5 aprobadas**, 4 archivos |
| `npm.cmd run test:e2e` en frontend | **3/3 aprobados**, 10.7 s, navegador America/Bogota |
| `npm.cmd run typecheck` y `npm.cmd run build` en frontend | Correctos |
| `manage.py check` | Sin problemas |
| `manage.py makemigrations --check --dry-run` | Sin cambios de modelos pendientes |
| `manage.py showmigrations --plan` | Todas las migraciones existentes aplicadas; no nuevas migraciones |

**Total final: 38 pruebas aprobadas y 0 fallidas en las suites finales.** Los tres fallos
iniciales de regresión permanecen documentados arriba. Se reinició solo el servidor Django
propio para que Playwright probara el código corregido. No se reinicializó PostgreSQL.

Los seis casos nuevos verifican medido con salida propia e idempotencia, estimado bloqueado,
simulado separado, intento de salida incompatible, salida histórica incompatible y exclusión
de acreditación estimada histórica sin borrar Verification. Panel y CSV coinciden por procedencia.
Los datos etiquetados medido/estimado de estas pruebas son fixtures sintéticos dentro de
test_ecogest: no mediciones de campo ni registros reales de la universidad.
Vitest adicional comprueba mensaje y opciones del gestor ante proceso estimado.
Las suites previas vuelven a comprobar masas, permisos, concurrencia, persistencia e integridad.

Rendimiento observado con el mismo escenario local: panel máximo de diez muestras 0.073 s,
CSV 0.589 s. No se extiende esa medición a todos los listados ni a producción.

CHK004 aprobado técnicamente con regla autorizada: **12/13**; CHK013 permanece pendiente.
Constitución vigente intacta y propuesta SVG 1.1.0 pendiente. Se creó hoja humana vacía y matriz
docente provisional; el PDF oficial aún no está disponible. No hay nuevo commit ni publicación.
T008/T014/T019/T026/T032 conservan su estado parcial por evidencia histórica TDD ausente.

## Ratificación y cierre documental posterior

Se ratifica constitución 1.1.0 con fecha 2026-11-15 por aprobación explícita del usuario.
Se ejecutaron resolve-template constitution-template y check-prerequisites con RequireSpec,
RequireTasks e IncludeTasks: ambos resolvieron correctamente. Sin hooks de extensiones.
Se revisó coherencia de constitución, 25 FR, 7 SC y 42 tareas; no se modifican las cinco
tareas TDD parciales. La lectura SDD distingue cobertura planificada de ejecución humana:
T038 no sustituye CHK013, ni T041 prueba rendimiento de todos los listados.
La guía de demo y hoja vacía se revisaron; no hay ejecución humana nueva.
Estos cambios son documentales: no se repitieron suites de software. La última evidencia
sigue siendo 38 aprobadas / 0 fallidas finales, con sus fallos iniciales preservados arriba.

## 2026-11-16 — Fase A Intelligence

Resultados y fallos preservados en [INFORME_FASE_A_V2.md](INFORME_FASE_A_V2.md).
Django 39/39, Vitest 7/7, Playwright 4/4: 50 pruebas finales aprobadas en esta fase.
TypeScript/build correctos. Observatorio p95 0.457 s, 10 000 registros, 10 lectores, 100 consultas.
Capturas reales bajo docs/evidencias/v2; simulaciones existentes, no mediciones reales.
Ninguna prueba de IA ni de fases futuras ejecutada; CHK013 y TDD histórico V1 sin cambios.


## 2026-11-16 — Refinamiento del Observatorio

Backend: 43/43 (76,059 s); Vitest: 9/9; Playwright: 5/5 (19,5 s).
Después se amplió el recorrido de refinamiento con contraste y teclado: 1/1 (3,4 s),
cinco textos representativos ≥5,43:1. TypeScript/build correcto. Cuatro anchos sin
desbordamiento, capturas antes/después preservadas e inspeccionadas.
Generador: documentado primero, pruebas antes del comando (3 errores y 1 paso por excepción
esperada), luego 4/4; ejecución local y repetición con misma huella, sin duplicados.
Observatorio p95 0,418 s; V1 p95 conservador 0,073 s; CSV 0,598 s.
Primer recorrido nuevo falló por selector de Área, corregido y validado. Sin migraciones.
Detalle reproducible, limitaciones y archivos en INFORME_REFINAMIENTO_OBSERVATORIO.md.
CHK013 pendiente; T008/T014/T019/T026/T032 históricas del MVP continúan parciales.


## 2026-11-16 — Ejecución final V2 en curso

Línea base repetida antes de B: backend 43/43 (82,511 s), Vitest 9/9, TypeScript correcto.
Observatorio p95 0,567 s; V1 p95 conservador 0,197 s, CSV 0,733 s.
Pasaporte: 3 pruebas previas a implementación, 2 fallos y 1 error por endpoint ausente;
después 3/3 (4,653 s). Casos saldo/traslado, acceso institucional/QR y salida compartida.
Build correcto tras UI B. Recorrido Playwright B 1/1 (6,2 s), capturas reales en
evidencias/v2/pasaporte a 360/390/768/1280, sin overflow; QR por teclado y vuelta a lista.
Primer intento de navegador falló porque el selector buscaba 87 sin unidad; corregido a 87 kg.
B aún requiere ampliar integración/accesos y revisar capturas antes de cerrar tarea y checkpoint.
C/D/E todavía pendientes de implementación. No llamada OpenAI ni prueba humana CHK013.


### Cierre técnico B y cálculo C

Pasaporte compacto con generaciones desplegables, acceso desde Registros (incluido hallazgo
del Observatorio→Registros), fuentes y QR. Capturas desktop/móvil inspeccionadas.
Simulador: cuatro pruebas previas fallaron con 404; tras implementación cinco pasan,
incluyendo 25/20/8 +3→23 acreditados hipotéticos, 2 pendientes y 92 %.
Regresión completa ejecutada: 51/51 backend (160,961 s), 12/12 Vitest, TypeScript/build
correctos, 7/7 Playwright (45,8 s). Observatorio p95 0,700 s; V1 p95 conservador 0,129 s;
CSV 1,207 s. Pasaporte+Simulador específicos 8/8 backend.
Cohorte simulada C: E=87 kg, hipótesis +10 muestra A'=110, G'=365 y tasa 30,14 %.
Rechazo de +88 kg, recarga de base y cuatro anchos sin desbordamiento verificados.
Capturas en evidencias/v2/pasaporte y evidencias/v2/simulador. Sin datos reales ni IA.
Pendiente C: transferencia manual a Planes (fase D). CHK013 sin ejecución humana.


### Planes D — pruebas del incremento

Antes de implementación: tres tests fallaron por rutas 404. Después, cinco tests de Planes
aprobados (43,180 s): permisos, versiones, historial, estados, evidencia, meta modificada,
fuente corregida, idempotencia y aislamiento. Con generador: 10/10 (86,436 s), incluida
repetición intacta tras recibo de plan. Vitest completa 14/14; TypeScript/build correctos.
Playwright escenario→plan→inicio→evaluación→cierre: 1/1 (17,6 s). Capturas reales en
evidencias/v2/planes (360/390/768/1280), sin overflow; revisión visual desktop realizada.
Base sintética de acreditación 60 kg (19 oct–1 nov), meta 90, observación 100 (2–15 nov):
alcanzada descriptivamente; no causalidad ni prueba humana. No consumo ambiental nuevo.
Respaldo restaurado y migración inicial de interventions ejecutada con éxito en copia y
luego desarrollo. manage.py check correcto; makemigrations --check --dry-run sin cambios.
Pendientes finales: concurrencia real entre gestores, regresión global después de E, revisión
visual móvil de Planes, enlaces documentales, CHK013 humana y pruebas pagadas IA no autorizadas.

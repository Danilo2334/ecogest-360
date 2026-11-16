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

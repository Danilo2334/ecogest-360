# EcoGest 360

MVP académico de gestión ambiental para una universidad: registro de residuos, lotes,
movimientos, compostaje verificado, indicadores y CSV. Un solo producto, con metodología SDD.

**Datos de demostración: simulados.** En esta versión, el aprovechamiento acreditado mide
solo entradas a compostaje cuyo proceso y destino validó un gestor. Las entregas externas
se muestran aparte y no se presumen aprovechadas. No se certifica calidad del compost.

Para acreditación real se exigen entradas medidas, salida pesada independientemente y evidencia
verificada por gestor. Los procesos estimados conservan trazabilidad, pero no se acreditan en
este MVP; regularizarlos requiere un procedimiento futuro aprobado. Los simulados solo aportan
al universo de demostración y no se convierten en mediciones reales al validarse.

## Stack y documentos

Python 3.12, Django 5.2 LTS, DRF y PostgreSQL 16. React, TypeScript, Vite y CSS Modules.
Dependencias Python fijadas en `backend/requirements.txt`; frontend en `frontend/package-lock.json`.

- [Constitución ratificada](.specify/memory/constitution.md)
- [Especificación](specs/001-ecogest-mvp/spec.md), [plan](specs/001-ecogest-mvp/plan.md)
- [Tareas y estado real](specs/001-ecogest-mvp/tasks.md)
- [Decisiones](docs/DECISIONES.md), [pruebas y límites](docs/PRUEBAS.md)

## Preparar desde cero — Windows PowerShell

Requiere Python 3.12, Node 22.12 o superior compatible y Docker Desktop funcionando.
No reinstalar Spec Kit. No modificar instalaciones Python globales.
Todos los comandos siguientes parten de la raíz del repositorio.
Se utiliza `npm.cmd` para no depender de la política de scripts de PowerShell.

```powershell
py -3.12 -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
py -3.12 scripts/configure_local.py
docker compose -p ecogest360 up -d db
docker compose -p ecogest360 ps
```

Esperar estado `healthy` de la base. El contenedor usa un volumen propio y escucha solo
en `127.0.0.1:55436`. Si el puerto está ocupado, elegir otro en `.env` y `compose.yaml`;
no detener servicios ajenos. `configure_local.py` crea secretos aleatorios en `.env` y no
sobrescribe un archivo existente. No publicar `.env` ni copiar sus valores a informes.

En una **base nueva de este proyecto**, crear una vez el rol limitado de aplicación:

```powershell
backend/.venv/Scripts/python.exe scripts/create_app_db_role.py
backend/.venv/Scripts/python.exe backend/manage.py migrate
backend/.venv/Scripts/python.exe backend/manage.py seed_demo
npm.cmd --prefix frontend ci
```

El script de rol prepara `ecogest_app` sin SUPERUSER ni CREATEROLE y actualiza `.env`
sin imprimir claves. Mantiene CREATEDB únicamente para bases de pruebas locales. Las claves
de bootstrap del contenedor quedan separadas de las de aplicación. No ejecutar este script
contra una base institucional existente. En una instalación ya preparada, omitirlo.

## Ejecutar

Terminal 1, desde raíz:

```powershell
backend/.venv/Scripts/python.exe backend/manage.py runserver 127.0.0.1:8000
```

Terminal 2, desde raíz:

```powershell
npm.cmd --prefix frontend run dev
```

Abrir **http://127.0.0.1:5178/**. Vite reenvía `/api` al backend local.
Si cambias el puerto web, actualizar también `CSRF_TRUSTED_ORIGINS`, `APP_ORIGIN` y las
pruebas Playwright. El puerto 5178 evita interferir con el servicio existente en 5173.
Este es un entorno de desarrollo local; no hay despliegue público.

### Cuentas de demo

`demo_administrador`, `demo_operador`, `demo_gestor`, `demo_consultor`.
La contraseña inicial es el valor **DEMO_PASSWORD de tu archivo `.env` local**;
consultarlo en el editor, sin publicarlo. `seed_demo` no reinicia contraseñas existentes.
El comando crea cuentas, campus, cafetería y catálogo demostrativo, pero no mediciones.
Las pruebas de navegador agregan registros explícitamente simulados y los conservan.

## Demostración funcional

1. Entrar con operador. En Registros crear 25 kg de orgánicos, área Cafetería,
   procedencia **simulado**, y conservar su identificador.
2. En Lotes asignar los 25 kg de ese registro a un lote; consultar QR y eventos.
3. En Compostaje iniciar proceso simulado e ingresar 20 kg del lote. Quedan 5 kg disponibles.
4. En Lotes intentar entregar 6 kg: se rechaza sin descuento. Una entrega de hasta 5 kg sí
   consume saldo, pero no cuenta como aprovechamiento acreditado.
5. Registrar controles opcionales y finalizar con 8 kg de salida **simulada e independiente**.
   Aportar referencia verificable o documento de destino también identificado como simulado.
6. Cerrar sesión. Entrar con gestor, revisar evidencia y confirmar explicando qué verificó.
7. Resumen muestra 25 kg generados, 20 kg de compostaje acreditado, 5 kg pendientes y 80 %
   para esa cohorte aislada. Nunca suma entrada y salida ni movimientos como generación.
8. Exportar CSV filtrado. Seleccionar solo medidos excluye todos esos registros.

Si ya hay otras demos, los totales acumulan todas las generaciones del filtro. No borrar
datos para forzar cifras: usar filtros o interpretar cada lote por su identificador.
El QR no evita login ni permisos; la URL local solo funciona donde el servidor sea accesible.

## Pruebas y comprobaciones

Desde raíz, con PostgreSQL disponible:

```powershell
backend/.venv/Scripts/python.exe backend/manage.py check
backend/.venv/Scripts/python.exe backend/manage.py makemigrations --check --dry-run
backend/.venv/Scripts/python.exe backend/manage.py test tests --noinput
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend run test -- --run
npm.cmd --prefix frontend run build
```

Desde `frontend`, con ambos servidores iniciados y demo preparada:

```powershell
npx.cmd playwright install chromium
npm.cmd run test:e2e
```

Las pruebas Django crean una base `test_ecogest` independiente y la eliminan al terminar;
no usan SQLite ni modifican los registros de desarrollo. Las pruebas de concurrencia usan
conexiones separadas. La prueba de rendimiento mide 10 000 registros simulados y 10 lectores.
Las pruebas de navegador dejan sus registros simulados en desarrollo. Capturas en
`frontend/test-results/` se excluyen de Git.

## Seguridad y operación

Sesión HttpOnly y CSRF, incluido login; permisos y filtrado institucional en servidor.
Administrador configura, operador captura, gestor valida y corrige lo permitido, consultor
solo lee. Correcciones de generación requieren que no existan asignaciones; el historial
conserva antes/después. Los errores históricos se registran como incidencias pendientes.

Los consumos son atómicos e idempotentes, con bloqueo PostgreSQL por lote y clave de operación.
Las cantidades son decimales, positivas, de hasta tres decimales en kg. No hay DELETE ambiental.
Los adjuntos se descargan autenticados, con límite 10 MiB y validación de PDF/JPEG/PNG;
no se ejecutan. La aplicación no sustituye un antivirus ni validación profesional del documento.

Para detener servidores usar Ctrl+C en sus terminales. `docker compose -p ecogest360 stop db`
conserva el volumen. **No usar `down -v` ni eliminar volúmenes con registros.**

## Límites de esta entrega

Una universidad administrable; la segunda institución solo aparece en fixtures de aislamiento.
Sin IA, IoT, PDF de informes, certificaciones, portal QR público ni reversión de consumos.
Los informes usan generación corregida vigente y corte de validación, no reconstrucciones
históricas de todas las correcciones. La acreditación se limita a compostaje.
Hay 12/13 criterios aprobados técnicamente; CHK013 sigue pendiente de demostración humana.
La aprobación académica no se deduce de los tests. La enmienda SVG está ratificada en constitución 1.1.0.
Consultar `docs/PRUEBAS.md` para resultados ejecutados y limitaciones de cobertura, sin asumir
que toda prueba planificada tiene evidencia histórica de una fase inicial fallida.


## Mapa documental vigente

- Gobierno: [constitución 1.1.0](.specify/memory/constitution.md).
- V2 vigente: [especificación](specs/002-ecogest-intelligence/spec.md),
  [plan](specs/002-ecogest-intelligence/plan.md), [tareas](specs/002-ecogest-intelligence/tasks.md),
  [diseño](docs/DISENO_EXPERIENCIA_V2.md).
- Fuentes canónicas de seguimiento: [decisiones](docs/DECISIONES.md), [pruebas](docs/PRUEBAS.md).
- Demo reproducible: [cohorte SIMULADA](docs/DATOS_DEMO_OBSERVATORIO.md);
  [guion académico](docs/DEMO_ACADEMICA.md) y [registro humano pendiente](docs/REGISTRO_DEMO_HUMANA.md).
- Evidencias visuales: [carpeta V2](docs/evidencias/v2/).
- Historia V1: [artefactos MVP](specs/001-ecogest-mvp/), auditoría y matriz docente en docs/.
- Plantillas originales: [constitución](docs/plantilla_constitucion_sdd.md),
  [especificación](docs/prompt_spec_template.md).

Los informes de fase A/refinamiento, diagnóstico preliminar, preparación de GitHub y propuestas
de PR son antecedentes, no fuentes del estado actual. Se conservan por trazabilidad académica.
El prompt maestro es brief de origen; spec.md tiene prioridad. Nuevos resultados se incorporan
a DECISIONES/PRUEBAS, sin crear un informe por ajuste.

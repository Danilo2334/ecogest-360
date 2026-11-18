# Preparación de Azure — 2026-11-17

Estado: publicación completada y cuatro casos de navegador aprobados en ejecuciones
remotas. Recursos creados con autorización explícita de USD 35/mes.
Las secciones de preparación conservan sus antecedentes.
Reinicio de la web y consulta posterior de la cohorte comprobados satisfactoriamente.

## Configuración efectiva autorizada

- Grupo: `rg-ecogest360-demo` (aislado de los recursos anteriores).
- Web: `ecogest360-d2334-1117`, App Service Linux B1, Central US.
- Base: `ecogest360-pg-d2334-ca`, PostgreSQL 16 B1ms/32 GiB, Canada Central.
- URL operativa: https://ecogest360-d2334-1117.azurewebsites.net
- Presupuesto de seguimiento `ecogest360-monthly35`: USD 35/mes, sin notificaciones
  ni corte automático. Se mantiene spendingLimit On de la oferta FreeTrial.
- Estimado base: web 0,018 × 730 = USD 13,14; DB 0,0185 × 730 = USD 13,505;
  almacenamiento 0,1265 × 32 = USD 4,048; **total USD 30,69/mes** redondeado.
  Transferencia interregional, impuestos y consumos extraordinarios no incluidos.
- Central US careció de disponibilidad real para PostgreSQL B1ms; East US 2 rechazó
  PostgreSQL y tiene cuota cero para web B1. Canada Central sí creó la base. Los intentos
  fallidos no dejaron otra base activa. Un solo plan web, una sola base operativa.
- Credenciales nuevas solo en `secrets/azure-access.json` y parámetros ignorados por Git.
  No copiar el contenido a Git, informes ni mensajes. `.env` local no se modifica.
- Migraciones y seeds existentes ejecutados sobre la base nueva. Cohorte Intelligence
  claramente SIMULADA. Claves de OpenAI no transferidas; asistente externo apagado.
- Trece IPs concretas de salida web admitidas por firewall. Regla temporal de bootstrap
  retirada. `ecogest_app` verificado sin SUPERUSER, CREATEDB ni CREATEROLE.
Login completado mediante navegador normal (broker deshabilitado solo para ese proceso).
Suscripción Azure subscription 1 activa; oferta FreeTrial_2014-09-01 y spendingLimit On
confirmados por ARM. El usuario declara USD 200 de crédito; saldo restante y vencimiento
no verificados. Existen recursos ajenos al proyecto que no se han modificado.
El presupuesto fue presentado y la creación aprobada posteriormente por el usuario.

## Antecedente: configuración propuesta inicialmente

| Recurso | Configuración |
| --- | --- |
| App Service | Linux B1, 1 instancia, Python 3.12, 2 workers Gunicorn |
| PostgreSQL | Flexible Server 16, Standard_B1ms, 32 GiB, backups 7 días, sin HA |
| Región | East US 2 propuesta: B1ms anunciado; East US restringida por la suscripción |
| Web | React compilado y API en un mismo origen HTTPS, dominio de Azure |
| Adjuntos | /home/ecogest/media persistente, descarga autorizada por API |
| IA externa | Deshabilitada, sin transferir clave local |

## Antecedente: presupuesto anterior a la validación regional

Tarifas USD recuperadas del HTML público oficial, campos `data-amount.regional.us-east-2`,
filas B1, B1ms y almacenamiento GiB/month. Retail Prices API respondió HTTP 429;
se usó la página oficial como fuente alternativa. Lectura 2026-11-17 Bogotá.

| Concepto | Tarifa | Estimado por 730 horas |
| --- | ---: | ---: |
| App Service Linux B1 | USD 0,017/h | USD 12,41 |
| PostgreSQL B1ms | USD 0,017/h | USD 12,41 |
| Almacenamiento PostgreSQL 32 GiB | USD 0,115/GiB-mes | USD 3,68 |
| **Base mensual** | | **USD 28,50** |

Presupuesto propuesto con margen: USD 35/mes para EcoGest; no es un límite automático
ni cotización contractual. No incluye impuestos, recursos existentes, IA, exceso de
transferencia o backups por encima de la franquicia. Backups incluidos hasta 100% del
almacenamiento provisionado; exceso LRS a USD 0,095/GiB-mes según la misma página.
No se descuentan beneficios gratuitos no confirmados. El crédito de prueba suele
vencer a los 30 días de activación; no interpretar USD 200 como siete meses garantizados.

Esta propuesta inicial fue sustituida por la configuración efectiva autorizada indicada
arriba. Microsoft.DBforPostgreSQL figuraba NotRegistered antes del aprovisionamiento;
posteriormente se registró con autorización del usuario.
La consulta de cuota Microsoft.Web devolvió BadRequest; la disponibilidad anunciada
de región/SKU no garantiza cuota de aprovisionamiento. No escalar a otro SKU sin revisar costo.

Fuentes: [App Service](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/),
[PostgreSQL](https://azure.microsoft.com/en-us/pricing/details/postgresql/flexible-server/).
Los presupuestos/alertas no son un corte duro de facturación. Detener una web no elimina
el costo de su plan; no prometer costo cero por detener el proceso.

## Herramientas y paquete

Azure CLI 2.93.0 instalada desde el ZIP oficial de Microsoft en
`%LOCALAPPDATA%/Programs/AzureCLI-2.93.0`; sin modificar Python global ni PATH.
Bicep CLI 0.49.2. Inicio de sesión del titular:

```powershell
$env:AZURE_CORE_ENABLE_BROKER_ON_WINDOWS='false'
$env:AZURE_CORE_LOGIN_EXPERIENCE_V2='off'
& "$env:LOCALAPPDATA/Programs/AzureCLI-2.93.0/bin/az.cmd" login --output none
```

El método con código de dispositivo fue rechazado por Security Defaults (AADSTS530035).
El navegador normal sí funcionó; no se deshabilitaron protecciones del directorio.
No compartir contraseña ni tokens.

Desde la raíz del repositorio:

```powershell
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-azure.txt
backend/.venv/Scripts/python.exe scripts/package_azure.py
backend/.venv/Scripts/python.exe scripts/check_azure_package.py
& "$env:LOCALAPPDATA/Programs/AzureCLI-2.93.0/bin/az.cmd" bicep build --file infra/azure/main.bicep --outfile build/azure/main.json
```

`build/azure/ecogest.zip` contiene solo código backend permitido, dependencias y build
frontend. No incluye .env, media, .git, tests, node_modules ni base local. Build y
plantilla compilada están ignorados por Git. El paquete fue enviado a Azure mediante
Azure CLI/Entra. Deployment activo: `71e0bd4c-2d6e-4048-b8ce-7675a80bb023`.

## Acceso y demostración

Usuarios: `intelligence_gestor` para observatorio, simulador, planes y asistente local;
`intelligence_administrador` para administración. Operación de pruebas V1 en la institución
separada de `demo_operador`/`demo_gestor`/`demo_consultor`/`demo_administrador`.
Contraseña nueva en el archivo local ignorado `secrets/azure-access.json`; no está en Git
ni coincide necesariamente con el DEMO_PASSWORD local. Todos los usuarios requieren login.

Para ver el observatorio de demostración, seleccionar procedencia **simulado**, desde
2026-11-02 hasta 2026-11-15: 365 kg generados, 100 kg acreditados, 265 kg pendientes, 27,40 %.
La cohorte se creó explícitamente con `seed_observatory_demo --apply --end-date 2026-11-15`.
La primera invocación sin --apply fue únicamente una vista previa y no creó usuarios;
se corrigió antes de validar el asistente. No se cambió la lógica del generador original.

OpenAI externo permanece apagado como en la configuración autorizada: consulta local
disponible, sin llamadas pagadas, sin cambiar el adaptador IA ni la configuración local.
El presupuesto Azure no autoriza gasto de OpenAI.

Pruebas de navegador: recorrido vertical con QR/compostaje/evidencia/CSV, consultor sin
formularios de escritura, teclado y cinco pantallas adaptables, asistente local en cuatro
anchos y enlace al simulador. Copias de pruebas existentes bajo frontend/test-results/azure-suite,
con credenciales cloud y destino remoto; archivos originales intactos. Capturas en test-results.
Detalle de fallos iniciales, correcciones y resultados en PRUEBAS.md.

## Pasos tras autenticación y aprobación de gasto

1. Verificar suscripción exacta, oferta/crédito, regiones, cuotas B1/B1ms y Python 3.12.
2. Elegir nombres disponibles; validar plantilla con Azure antes de crear en un grupo nuevo.
3. Generar secretos nuevos; usar parámetros seguros y no imprimir respuestas con credenciales.
4. Crear infraestructura. La plantilla deja PostgreSQL sin reglas de acceso: agregar solo
   IPs de salida de la app y, temporalmente, la IP de aprovisionamiento. No abrir a todo Azure.
5. Crear `ecogest_app` sin privilegios de administrador, CREATEDB ni CREATEROLE; darle
   propiedad/permisos únicamente de la base/esquema ecogest para migraciones.
6. Aplicar migraciones explícitas a esa base nueva con TLS y retirar el acceso temporal.
   No ejecutarlas al arrancar cada worker ni cargar datos locales automáticamente.
7. Tomar `defaultHostName` real devuelto por Azure y actualizar `AZURE_APP_HOST`.
8. Desplegar ZIP mediante Azure CLI autenticada con Entra; publicación básica/FTP deshabilitada.
9. Crear usuarios y datos de demostración solo según alcance acordado. Revisar autenticación,
   permisos, QR, saldo insuficiente, compostaje y reportes desde navegador remoto.
10. Reiniciar y verificar persistencia. Antes de datos reales, preparar respaldo de adjuntos
    independiente de PostgreSQL. Registrar URL y pruebas reales en PRUEBAS.md.

## Límites de la preparación

Build/TypeScript, 18 pruebas frontend, 4 pruebas de paquete, check Django local y compilación
Bicep aprobados. Check de producción con clave temporal fuerte: solo advertencia W021
porque no se solicita HSTS preload para este dominio inicial. HSTS usa 3600 segundos.
No se ejecutó Gunicorn en Linux: Docker Desktop no tenía motor disponible. Tampoco se
probó conectividad PostgreSQL Azure, migraciones remotas, despliegue ni flujo E2E remoto.
La compilación Bicep no demuestra cuotas o disponibilidad del servicio.

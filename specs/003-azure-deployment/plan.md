# Plan de despliegue Azure

App Service Linux B1 (una instancia, Python 3.12, Gunicorn) sirve API y build React en
un mismo origen HTTPS. WhiteNoise sirve únicamente assets públicos; Django conserva
autorización de adjuntos bajo /home/ecogest/media. PostgreSQL Flexible Server 16,
Burstable B1ms, 32 GiB, backups locales 7 días, sin alta disponibilidad.

Despliegue autorizado por el usuario con presupuesto estimado de USD 35/mes.
Web en Central US y base en Canada Central por restricciones de cuota/capacidad.
East US 2 carece de cuota B1 web; PostgreSQL falló en Central US y East US 2 antes
de quedar operativo en Canada Central. Se conserva un solo plan y una sola base activa.
Base mensual estimada USD 30,69, más transferencia interregional y consumos extraordinarios.
Login y oferta FreeTrial con spendingLimit On verificados; saldo/vencimiento no confirmados.
Plantilla infra/azure/main.bicep con databaseLocation independiente.

Secuencia: login → inventario/estimado → aprobación → grupo nuevo → plantilla →
firewall solo IPs de salida web y acceso temporal de aprovisionamiento → rol limitado
ecogest_app → migraciones explícitas → retirar acceso temporal → ZIP → pruebas remotas.
El dominio real devuelto por Azure debe actualizar AZURE_APP_HOST antes de las pruebas.
No automatizar seed ni copiar la base local. No iniciar migraciones en cada arranque.

Credenciales nuevas solo en parámetros seguros/variables de proceso; ninguna salida debe
mostrarlas. No colocar la credencial administradora de PostgreSQL en la aplicación.
El rol de app debe tener LOGIN/NOSUPERUSER/NOCREATEDB/NOCREATEROLE y permisos solo sobre
ecogest. Ajustar propiedad del esquema público para migraciones de ese rol.

Validación: build/TypeScript, checks Django de producción, pruebas de enrutamiento,
assets, HTTPS y exclusión de secretos del ZIP; compilación Bicep local. Después de aprobar:
validación ARM, cuotas, instalación Linux, migraciones y recorrido remoto completo.

Los backups de PostgreSQL no incluyen adjuntos: establecer respaldo de /home/ecogest/media
antes de usar datos reales. Piloto de demostración sin SLA propio ni promesa de alta disponibilidad.

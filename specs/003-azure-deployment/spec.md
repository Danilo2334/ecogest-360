# Despliegue académico en Azure

Solicitud del usuario: preparar Azure CLI y el despliegue; presentar costos antes de crear
recursos. Preparación local autorizada el 2026-11-17. Posteriormente el usuario autorizó
crear recursos y desplegar con presupuesto estimado de USD 35/mes, preservando app,
configuración local de IA y repositorio. No autoriza consumo adicional de OpenAI.

## Features principales

### 1. Acceso remoto al piloto
- Publicar EcoGest mediante HTTPS, conservando autenticación, roles, aislamiento y QR privado.
- Mantener todos los flujos y reglas ambientales V1/V2, sin cambiar sus indicadores.
- Conservar datos y adjuntos al reiniciar la aplicación.

### 2. Operación controlada
- Preparar un paquete reproducible sin secretos, base local ni adjuntos privados.
- Usar una base nueva; no copiar registros ni crear datos de demo automáticamente.
- Mantener el asistente externo deshabilitado y no cargar su clave.
- Presentar configuración y costo antes de provisionar; verificar suscripción, crédito y región.
- Verificar login, permisos, recorrido ambiental y persistencia después del despliegue.

## Non-Goals
- Publicación multiinstitución, dominio pagado, cambios de stack o lógica ambiental.
- Push/merge, migraciones destructivas, uso de IA pagada y traslado de datos privados.
- Declarar el despliegue completado sin probar el servicio remoto.

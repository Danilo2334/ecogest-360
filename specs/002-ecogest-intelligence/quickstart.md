# Verificación V2

Desde raíz, con PostgreSQL activo y migraciones aditivas D/E aplicadas según README, sin borrar datos:

```powershell
backend/.venv/Scripts/python.exe backend/manage.py test tests --noinput
npm.cmd --prefix frontend run test -- --run
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend run build
Push-Location frontend
npm.cmd run test:e2e
Pop-Location
```

Backend 8000 y frontend 5178 activos antes de Playwright; README conserva instrucciones.
Pruebas backend usan base test separada; navegador V1 registra nuevas simulaciones identificadas.
Capturas V2 de datos existentes, filtros explícitos, sin contraseñas ni .env.
Esperado: contrato V1 intacto, comparación solo completa, filtros por procedencia/área, sin overflow
360/390/768/1280; roles y logout. No interpretar las capturas como mediciones reales.
A–E implementadas localmente. Las llamadas OpenAI usan mocks; presupuesto y smoke real pendientes. CHK013 sigue pendiente.
Preparar seed_observatory_demo explícitamente antes de los recorridos V2. Capturas actuales
en docs/evidencias/v2/integracion y docs/evidencias/v2/asistente; originales de fases preservados.

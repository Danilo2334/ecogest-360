# Verificación V2

Desde raíz, con PostgreSQL existente activo, sin borrar datos ni migrar en A:

```powershell
backend/.venv/Scripts/python.exe backend/manage.py test tests --noinput
npm.cmd --prefix frontend run test -- --run
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run test:e2e
```

Backend 8000 y frontend 5178 activos antes de Playwright; README conserva instrucciones.
Pruebas backend usan base test separada; navegador V1 registra nuevas simulaciones identificadas.
Capturas V2 de datos existentes, filtros explícitos, sin contraseñas ni .env.
Esperado: contrato V1 intacto, comparación solo completa, filtros por procedencia/área, sin overflow
360/390/768/1280; roles y logout. No interpretar las capturas como mediciones reales.
Las fases futuras requieren sus propias pruebas y autorización. CHK013 sigue pendiente.

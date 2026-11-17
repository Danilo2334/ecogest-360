# Cohorte reproducible del Observatorio — SIMULADO

Diseño aprobado 2026-11-16. No son mediciones ni evidencia de campo.

Comando previsto: `backend/.venv/Scripts/python.exe backend/manage.py seed_observatory_demo`.
Sin opciones presenta el plan sin escribir. `--apply --end-date 2026-11-15` crea una sola cohorte;
`--describe` consulta el manifiesto existente. Ejecutar únicamente después de las pruebas del comando.

Institución reservada: `DEMO INTELLIGENCE · SIMULADO · v1`. Usuarios nuevos `intelligence_administrador`,
`intelligence_operador`, `intelligence_gestor`, `intelligence_consultor`; contraseña inicial desde
DEMO_PASSWORD local, nunca impresa ni versionada. Las cuentas demo anteriores conservan su institución.

84 registros: 28 días × tres áreas. Primer período de 14 días: base diaria 8/5/3 kg;
segundo: 12/6/4 kg, respectivamente Cafetería/Aulas/Oficinas. Cada base suma día-del-período módulo 4.
Materiales respectivos: orgánicos / papel y cartón / no aprovechables. Dos lotes orgánicos, cada uno
asigna la generación de su período; entrada a compostaje de 60 kg y 100 kg, salidas independientes
de 19 kg y 31 kg, con evidencia y validación expresamente simuladas. No presupone rendimiento real.

Fechas de generación son parte del escenario sintético; creación, movimientos y verificación conservan
el reloj real, sin falsificar timestamps. Comparar generaciones históricas no simula antigüedad del
compostaje. Se usan los servicios de dominio existentes y una transacción con bloqueo de comando.
Ante nombre de usuario o institución preexistente sin manifiesto, aborta; no adopta cuentas.
El manifiesto guarda fechas e IDs en auditoría. Repetir no altera ni restablece nada; si cambió la
cohorte o se solicita otro período, informa el conflicto. No hay opción force ni borrado.

No se ejecuta automáticamente al arrancar. Para ver la cohorte: entrar con una cuenta intelligence,
seleccionar Simulado y el segundo período del manifiesto. Corte actual incluye la validación simulada.
Las capturas deben identificar la procedencia y no certificar prueba humana CHK013.

# Guion de demostración — solo simulaciones

Duración sugerida: 10–15 minutos. Servidores locales y PostgreSQL activos según README.
No mostrar .env, contraseñas, consola con credenciales ni datos personales en la grabación.
Utilizar cuentas demo; toda masa, comprobante y confirmación debe declararse SIMULADA.

Preparación por el responsable antes de empezar (desde la raíz):

```powershell
docker compose -p ecogest360 start db
backend/.venv/Scripts/python.exe backend/manage.py runserver 127.0.0.1:8000
```

En otra terminal: `npm.cmd --prefix frontend run dev`. Si los servicios ya están activos,
no duplicarlos. Abrir http://127.0.0.1:5178/. Cuentas: demo_administrador, demo_operador,
demo_gestor y demo_consultor; consultar DEMO_PASSWORD local sin mostrarlo en capturas.
No ejecutar migraciones ni reinicializar datos para este ensayo. Preparar la hoja
REGISTRO_DEMO_HUMANA.md y entregar el guion escrito; el observador no guía verbalmente.
El catálogo se mantiene como demostrativo y no oficial. No marcar la ejecución por anticipado.

1. Mostrar constitución, spec y tasks; explicar cinco módulos y las cinco tareas TDD parciales.
2. Administrador: mostrar catálogo demostrativo y cuatro roles, sin afirmar catálogo oficial.
   Crear un área nueva `DEMO AUDITORÍA <fecha-hora>` en la sede piloto para aislar esta cohorte.
3. Operador: registrar **25 kg simulados** de orgánicos en esa área. Anotar ID del registro.
   Intentar 0 o -1 kg y mostrar rechazo; no cambiar la procedencia a medido.
4. Crear lote de 25 kg. Consultar identificador y PNG QR. La lectura por cámara queda pendiente;
   la consulta requiere sesión y el enlace local no sirve automáticamente desde otro dispositivo.
5. Registrar movimiento logístico de 20 kg: conserva 25 kg disponibles y G=25.
6. Iniciar proceso SIMULADO e ingresar 20 kg del lote: saldo 5. Intentar entrega de 6 kg:
   rechazo, saldo continúa en 5. Una entrega válida de 5 kg deja disponible 0, pero no acredita.
7. Finalizar proceso con salida independiente **8 kg simulados** y destino Huerta DEMO.
   Adjuntar referencia `ACTA-SIMULADA-<id>` y receptor/fecha/descripción completos.
   Antes de validación: A=0. No presentar comprobante simulado como evidencia de campo.
8. Gestor: revisar y confirmar con motivo que indique expresamente la simulación. No crear
   movimientos con este rol. A=20, nunca 28 ni 8.
9. Panel: filtrar por área nueva y procedencia simulado. G=25, A=20, pendiente=5, tasa=80 %.
   Si se entregaron los 5 kg: entregado=5 y disponible=0. Si no: entregado=0 y disponible=5.
   Mostrar fórmula, corte, etiqueta provisional y que el indicador solo acredita compostaje.
10. Exportar CSV filtrado y contrastar filas y totales; seleccionar medido en esa área debe
    mostrar vacío/No calculable. No borrar demos previas para forzar cifras.
11. Consultor: consultar sin formularios de escritura. Cerrar sesión y verificar acceso denegado.
12. Mostrar informe de pruebas, capturas y limitaciones. Explicar que hay cuatro commits locales (dos por autor registrado),
    pero publicación y colaboración verificable mediante PRs aún están pendientes.

Registrar quién ejecutó la demo, fecha, navegador, IDs y resultados observados. Un ensayo
automatizado no reemplaza la validación humana sin ayuda oral de SC-006.

# Guion de demostración — EcoGest 360 Intelligence V2

Recorrido audiovisual de 10–15 minutos. Todo lo mostrado es SIMULADO, nunca medición
ambiental real. CHK013 requiere que una persona lo ejecute sin ayuda oral; las capturas
Playwright no sustituyen ese registro. No grabar claves, `.env`, contraseñas ni datos privados.

## Preparación fuera de cámara

Seguir README para instalación, migraciones y servidores. Si ya están activos, no duplicarlos.
En una terminal raíz: `backend/.venv/Scripts/python.exe backend/manage.py runserver 127.0.0.1:8000`.
En otra: `npm.cmd --prefix frontend run dev`. Abrir http://127.0.0.1:5178/.
La cohorte se prepara explícitamente con `seed_observatory_demo`, documentada en
[DATOS_DEMO_OBSERVATORIO.md](../evidencias/DATOS_DEMO_OBSERVATORIO.md); repetir verifica integridad sin
resembrar. No editar ni borrar sus registros para ajustar cifras. Usar otras áreas para
ensayos operativos nuevos. Cuentas intelligence_gestor e intelligence_consultor, contraseña
local DEMO_PASSWORD que el responsable consulta sin compartir ni grabar. No activar OpenAI.

## Recorrido V2 (12–14 minutos)

| Tiempo | Acción y explicación | Comprobación observable |
| --- | --- | --- |
| 0–1 min | Presentar EcoGest: registro → evidencia → decisión; SDD y constitución 1.1.0. | Mostrar spec/plan/tasks V2; cinco tareas TDD V1 siguen parciales. |
| 1–3 min | Entrar con intelligence_gestor. Observatorio: procedencia simulado, 2–15 nov 2026, todas las áreas/materiales, corte vacío. | 365 kg generados, 100 acreditados, 265 pendientes, 27,40 %. El indicador solo acredita compostaje. |
| 3–4 min | Abrir el hallazgo de Cafetería y su evidencia; explicar que el ranking usa masa absoluta, no tasa por persona. | Área Cafetería 187 kg; filtros conservados en Registros. |
| 4–6 min | En Registros seleccionar una generación orgánica asignada a lote y abrir su pasaporte; alternativamente Trazabilidad. Abrir fuentes, proceso y QR. | Fechas/actores registrados, saldo y ramas. Entrada no se suma a salida independiente; QR exige sesión. |
| 6–8 min | Volver a Observatorio y restablecer cohorte completa de 2–15 nov, simulado. Abrir Simulador; aumento hipotético de 10 kg. | Base G=365/A=100; elegible 87; resultado G'=365/A'=110/pendiente'=255/tasa 30,14 %. No cambia el Observatorio. Intentar 88: rechazo. |
| 8–10 min | Para demostrar evaluación, cambiar base a 19 oct–1 nov, simulado, área Cafetería. Simular +10 kg → Revisar propuesta de plan. Elegir responsable intelligence_gestor, indicador compostaje acreditado, meta mínima 90 kg, plazo 31 dic 2026, problema/acción/motivo claramente SIMULADOS. Guardar y abrir el plan. | Base 60 kg conservada al iniciar. La simulación no garantiza la meta; requiere acción y evidencia posteriores. Solo gestor escribe. |
| 10–11 min | Iniciar → pasar a evaluación. Registrar seguimiento humano simulado. Evaluar período 2–15 nov, mismo ámbito, con motivo. | Observación acreditada 100 kg frente a meta 90: meta alcanzada observada. Comparación sintética, no éxito causado por el plan. Cerrar requiere evaluación vigente. |
| 11–13 min | Abrir Asistente con los mismos filtros. Mostrar fuentes y desplegar metodología local. Preparar preguntas sugeridas de los tres modos. | OpenAI no disponible: no se finge una respuesta de IA. Datos locales consultables. Cerrar sesión y entrar como intelligence_consultor: no puede editar planes. |
| 13–14 min | Mostrar pruebas/capturas, límites y pendientes humanos. | Dos consultas OpenAI reales verificadas desde Django en docs/PRUEBAS.md; servicio desactivado, recorrido del navegador con IA real pendiente. CHK013 y revisión académica pendientes. |

Si un valor difiere, registrar filtros y resultado observado; no inventar el resultado ni borrar
información. Los planes de ensayo pueden conservarse cerrados/cancelados con motivo; no son
mediciones nuevas. Los botones de creación no aparecen con consultor/administrador/operador.
Las fechas ISO de formularios se acompañan con período explicativo; el navegador puede mostrar
mes/día en controles nativos aunque el texto esté en español.

Preguntas preparadas para una futura prueba OpenAI **solo después de autorización de presupuesto**:
«¿Qué área produjo más residuos?», «¿Cuánto está acreditado y pendiente?»,
«¿Por qué no sumamos entrada y salida de compost?», «¿Qué debo revisar primero?».
El modelo selecciona fuentes y explicaciones del catálogo validado; no ejecuta acciones,
no hace búsqueda web, no responde con cifras propias. Fuera del catálogo declara insuficiencia.
Cambiar filtros deja la respuesta anterior identificada con su contexto; salir limpia la conversación.

Las dos consultas autorizadas del 2026-11-16 ya están registradas en
[PRUEBAS.md](../PRUEBAS.md), con consumo y fuentes verificadas. Fueron ejecutadas desde Django;
no deben presentarse como prueba de este recorrido en navegador. La demostración mantiene
OpenAI desactivado y no autoriza llamadas adicionales.

Registrar ejecutor, observador, fecha, duración, dificultades, IDs y capturas observadas en
[REGISTRO_DEMO_HUMANA.md](REGISTRO_DEMO_HUMANA.md), sin marcar aprobación anticipada.
Conservar CHK013 pendiente hasta ejecución humana real. Cada integrante prepara su entrega
individual en Campus UCC y verifica sus contribuciones/revisión de PR con su cuenta.

## Recorrido operativo V1 conservado (alternativo: otros 10–15 minutos)

Este segundo guion verifica captura y acreditación desde cero en una cohorte nueva.
No se suma al tiempo del video V2 ni se ejecuta dentro de la institución del seed protegido.

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
docs/entrega/REGISTRO_DEMO_HUMANA.md y entregar el guion escrito; el observador no guía verbalmente.
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
12. Mostrar informe de pruebas, capturas y limitaciones. Mostrar el historial Git vigente y distinguir autoría registrada de revisión colaborativa verificable.
    La V2 de esta ejecución es local; no afirmar revisión ni merge del PR por enseñar commits.

Registrar quién ejecutó la demo, fecha, navegador, IDs y resultados observados. Un ensayo
automatizado no reemplaza la validación humana sin ayuda oral de SC-006.

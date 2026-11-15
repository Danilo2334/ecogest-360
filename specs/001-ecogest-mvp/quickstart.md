# Guía de validación prevista

No ejecutada: aún no existen aplicación, dependencias ni migraciones. Estos comandos son
el contrato de arranque que deberá entregar la implementación, no una afirmación de funcionamiento.

## Prerrequisitos y preparación posterior a aprobación

Comprobar `py -3.12 --version`, `node --version`, `npm --version`, `psql --version`.
El implementador elegirá versión compatible de Node con Vite y la documentará junto a lockfiles.
PostgreSQL local o contenedor existente; no instalar ni modificar servicios globales sin revisar.
Crear base y usuario local de mínimo privilegio; usuario de pruebas debe poder crear base de test.
Copiar `.env.example` a `.env` y configurar valores localmente, nunca en Git ni en capturas.

Desde raíz, comandos previstos para PowerShell:

```powershell
py -3.12 -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
backend/.venv/Scripts/python.exe backend/manage.py migrate
backend/.venv/Scripts/python.exe backend/manage.py seed_demo
backend/.venv/Scripts/python.exe backend/manage.py test
backend/.venv/Scripts/python.exe backend/manage.py runserver 127.0.0.1:8000
```

Otra terminal en frontend:

```powershell
npm ci
npm run typecheck
npm run test -- --run
npm run build
npm run dev -- --host 127.0.0.1
```

Playwright se instalará solo durante implementación autorizada; `npm run test:e2e` ejecutará
el flujo con ambos servidores. Seed demo pedirá contraseñas o leerá variables locales:
sin contraseñas conocidas en el repositorio, sin crear datos medidos ni duplicar ejecuciones.

## Recorrido de aceptación

1. Administrador prepara piloto, usuarios y catálogo demo; verificar que consultor no escribe.
2. Operador registra 25 kg orgánicos simulados, crea lote y asigna 20 a compostaje.
3. Comprobar saldo 5; rechazar 6 kg, cero, negativo y exceso de precisión.
4. Reenviar misma operación: un consumo. En prueba PostgreSQL separada, dos consumos de
   4 sobre 5 dejan un éxito, un conflicto y saldo 1; no usar el lote de la demo principal.
5. Registrar salida independiente de 8 kg simulados, finalizar; sin evidencia A=0.
6. Gestor verifica registro de proceso, salida, fecha, responsable y destino simulado:
   A=20, G=25, tasa=80 %, pendiente=5; nunca G=45 o A=28. Repetir validación no duplica.
7. Filtrar solo medidos: la demo desaparece; denominador cero produce «No calculable».
8. Exportar CSV con filtros/corte iguales y comparar valores manualmente; comprobar textos
   con comas, comillas, saltos, tildes y apariencia de fórmula.
9. Intentar corregir generación asignada: rechazo; registrar incidencia histórica sin alterar saldo.
10. Reiniciar servidores, volver a autenticar y recuperar datos; comprobar acceso cruzado usando
    una segunda institución solo en fixtures de aislamiento, no en administración del piloto.

## Evidencia de cierre

Registrar comandos, versiones, resultados y fallos en docs/PRUEBAS.md. Verificar migraciones
en base vacía y ausencia de cambios de modelo sin migración. Registrar pruebas de CSRF,
401/403/404, acceso privado a evidencia y QR; teclado y anchuras 360/1280 de SC-006.
No declarar terminada una historia hasta ver su recorrido persistido y probar errores relevantes.

# Decisiones técnicas — EcoGest 360

Fecha: 2026-11-15. Investigación documental; no instalación ni prueba de aplicación.

## Sesiones y permisos

Decisión: sesión Django, cookie HttpOnly, CSRF también en login, proxy Vite hacia servidor
para mismo origen lógico. HTTPS y cookie Secure al configurar un entorno HTTPS; local solo
loopback. DRF SessionAuthentication se adaptará con authenticate_header para emitir 401
con WWW-Authenticate ante falta de sesión; permisos y CSRF denegados devuelven 403.
Motivo: respetar constitución y evitar tokens persistentes en almacenamiento del navegador.
Alternativa: JWT, descartada por revocación y complejidad innecesarias para este piloto.
Fuente: https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication

## Masa, transacciones y reintentos

Decisión: Decimal y numeric, contratos con cadenas decimales; 12 dígitos totales, 3 decimales
en kg como límite técnico inicial, sin redondeo silencioso. Rechazar exceso de precisión.
Los servicios de dominio usarán atomic y select_for_update sobre generación/lote/proceso,
en orden estable por tipo e identificador. Un consumo y su evento se guardan juntos.
Una clave de operación única por institución, actor y tipo conserva el hash normalizado de
entrada y resultado. Mismo contenido repite resultado; diferente contenido produce conflicto.
La clave y el efecto se confirman juntos; la carrera sobre clave única se resuelve después
de rollback leyendo el resultado ganador. Nunca continuar una transacción rota.
Alternativas rechazadas: floats, validación de saldo fuera de transacción, solo deshabilitar botón.
Fuentes: https://docs.djangoproject.com/en/5.2/topics/db/transactions/
https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update
https://docs.djangoproject.com/en/5.2/ref/models/fields/#decimalfield
https://www.postgresql.org/docs/current/datatype-numeric.html

## Verificación de concurrencia

Decisión: TransactionTestCase con conexiones independientes y PostgreSQL real. Barrera de
sincronización controlada, límite de espera y propagación de excepciones de cada trabajador.
Comprobar un éxito, un conflicto y saldo 1 cuando dos consumos de 4 compiten por saldo 5.
Alternativas rechazadas: TestCase transaccional envolvente y SQLite, que no prueban estos bloqueos.
Fuente: documentación select_for_update anterior.

## Interfaz y compilación

Decisión: React, TypeScript, Vite y CSS Modules, CSS global solo para bases y variables.
Chequeo TypeScript separado de la compilación; Vitest/Testing Library para formularios y
Playwright para recorrido real. Gráficos SVG simples con tabla equivalente, sin biblioteca
adicional mientras no haga falta. La selección exacta de versiones se fijará en lockfiles
durante implementación tras verificar compatibilidad; no se inventa una instalación actual.
Fuentes: https://vite.dev/guide/features.html#css-modules
https://vite.dev/guide/features.html#typescript

## Evidencia e indicadores

Decisión de diseño derivada de Q3: validación única por proceso y entradas inmutables al
finalizar. El numerador agrupa entradas por origen y fecha de validación, nunca salidas.
Documentos privados fuera de directorios públicos; aceptar PDF/JPEG/PNG hasta 10 MiB,
verificando contenido y acceso, sin ejecutar archivos. Alternativa: enlaces públicos,
rechazada porque el comprobante puede contener información institucional.
Los límites técnicos son propuestas del plan, no nuevas certificaciones ambientales.

## Entorno

Python 3.12, Django 5.2 LTS, DRF, PostgreSQL 16 como objetivo local; no exigir Docker.
Comprobar versiones disponibles antes de instalar en un entorno aislado autorizado.
No modificar Python global. Si falta PostgreSQL, documentar opción local o contenedor
antes de ejecutar. No se ha comprobado aún disponibilidad del entorno de implementación.

# AGENTS.md — EcoGest 360 · Proyecto académico SDD

## Propósito y contexto
- Repositorio ya inicializado con GitHub Spec Kit. NO ejecutar `specify init` de nuevo ni borrar `.specify/`, `.github/` o datos existentes.
- Un solo producto: EcoGest 360. Integra gestión de residuos (EcoGest), trazabilidad de lotes y QR (idea TraceFood) y aprovechamiento orgánico/compostaje (idea AgroPilot). Piloto de una universidad, con arquitectura extensible.
- Este proyecto tiene dos destinos académicos: Ingeniería Web (SDD + artefactos, Git, pruebas, demo) e Ingeniería Ambiental (registro, caracterización e indicadores honestos).
- Lee `docs/historico/01_VISION_Y_ALCANCE_ECOGEST360.md`, `docs/historico/02_CONSTITUCION_PROPUESTA_ECOGEST360.md`, `docs/historico/03_ALCANCE_MVP_ECOGEST360.md` y las plantillas docentes antes de decidir o modificar.
- Las plantillas de la profesora tienen prioridad sobre propuestas informales; respeta sus seis apartados constitucionales y lista de verificación.

## Fuente de verdad y alcance
1. Constitución aprobada en `.specify/memory/constitution.md`; especificaciones funcionales bajo `specs/` en `spec.md`; plan y tareas según Spec Kit. Ante contradicción crítica, detener ese cambio e informar.
2. El alcance prioritario propuesto para la primera entrega se define en `docs/historico/03_ALCANCE_MVP_ECOGEST360.md`. No transformar ideas futuras en funcionalidades actuales sin aprobación del usuario.
3. No confundir especificación funcional con plan técnico: `spec.md` debe describir qué, para quién, reglas, criterios medibles y Non-Goals; sin endpoints ni estructura SQL.
4. La solicitud del estudiante autoriza crear artefactos SDD y desarrollar el MVP aprobado, de modo incremental y comprobable, sin exigir confirmación para cada edición normal. No autoriza acciones destructivas o exposición de secretos.

## Stack acordado para preparar plan técnico
- Frontend: React + Vite + TypeScript, diseño web responsive y accesible.
- Backend: Python (preferir versión 3.12/3.13 local si está disponible), Django 5.2 LTS + Django REST Framework.
- Persistencia: PostgreSQL con ORM y migraciones de Django. No cambiar stack en silencio.
- Si una dependencia o herramienta falta, comprobar instalación y ofrecer alternativa documentada; no romper instalaciones Python globales existentes.
- No convertir la integración de Gemini/otros LLM en requisito para iniciar el sistema. Es mejora posterior y requiere clave en `.env`, nunca en Git.

## Reglas de dominio que NO pueden romperse
- Pesos positivos, con aritmética decimal y unidades claras (kg); las masas nunca se inventan.
- No mover, entregar ni ingresar a compostaje más masa que la disponible en el lote. Evitar doble aplicación por solicitudes repetidas o simultáneas.
- Movimientos y recolecciones NO son nueva generación. Indicadores no deben contar doble la misma masa.
- Diferenciar registros medidos, estimados y simulados. Los simulados nunca se exhiben como mediciones reales.
- Diferenciar potencialmente aprovechable de aprovechamiento efectivamente verificado; documentar fórmula, corte y universo de cada indicador.
- Compostaje: registrar masas de entrada y salida por separado; no presuponer rendimiento ni certificar calidad del compost.
- Control de acceso en backend, mínimo privilegio y sin visibilidad de datos ajenos.
- Correcciones auditadas; no borrar silenciosamente información ambiental validada.
- QR solo identifica lotes sin incluir claves o datos sensibles; no sustituye permisos.
- Separación en fuente ordinaria blanco/verde/negro aplicable en Colombia; no asignar peligrosos o especiales como ordinarios ni afirmar certificación legal.

## Calidad, pruebas y evidencias
- Verificar que el entorno arranque de cero siguiendo README, con `.env.example` seguro y migraciones reproducibles.
- Probar por lo menos autenticación/autorización, validación de masas, saldos insuficientes, duplicación/doble conteo, registro y recuperación, permisos, compostaje y dashboard.
- No declarar "probado" un caso sin ejecutar la prueba o procedimiento y registrar el resultado; reportar límites y pendientes sin ocultarlos.
- Priorizar un flujo vertical completo sobre cinco pantallas incompletas. Registrar decisiones relevantes en `docs/DECISIONES.md` y resultados en `docs/PRUEBAS.md`.
- Registrar commits por hitos coherentes y PRs revisables; NO fabricar autores, timestamps, resultados, revisiones ni contribuciones. Las identidades reales de Github son `Danilo2334` y `francisco3788`; no usar `Camm001E` en este proyecto. Comprobar qué cuenta está activa y la configuración Git antes de cualquier push. Los participantes reales deben verificar/autorizar las contribuciones que se les atribuyen.
- No exponer ni imprimir tokens, claves, credenciales o información privada.

## Política de ejecución con tiempo limitado
- Prioridad estricta: 1) especificaciones coherentes, 2) backend funcionando con reglas, 3) flujo web completo, 4) pruebas y README, 5) extras.
- Nunca reemplazar funcionalidad real por datos visuales falsos. Si el tiempo impide una característica, documentarla como pendiente y asegurar que el MVP restante es funcional.
- No hacer push, PR merge, despliegue público, gasto en servicios o cambios destructivos sin autorización explícita para esa acción.

# INSTRUCCIONES PARA PEGAR EN CODEX (modo local / extensión / escritorio)

Actúa como arquitecto full-stack, analista SDD, implementador y QA del proyecto **EcoGest 360**. Tengo una ventana de trabajo de aproximadamente cinco horas para preparar una primera entrega académica demostrable. Se autoriza avanzar de forma autónoma por las **fases documentales y el MVP delimitado**, ejecutando pruebas e informando resultados, sin pedir aprobación para cada edición ordinaria.

**Antes de tocar código:**
1. Confirma la carpeta raíz actual y el estado Git; examina la estructura actual y preserva `.specify/`, `.github/`, `.vscode/` y cualquier trabajo ya existente. No ejecutes `specify init --here --force`.
2. Lee completos `AGENTS.md`, `docs/01_VISION_Y_ALCANCE_ECOGEST360.md`, `docs/02_CONSTITUCION_PROPUESTA_ECOGEST360.md`, `docs/03_ALCANCE_MVP_ECOGEST360.md`, `docs/04_PLAN_DE_EJECUCION_Y_EVIDENCIAS.md`, `docs/plantilla_constitucion_sdd.md` y `docs/prompt_spec_template.md`.
3. Inspecciona las habilidades Spec Kit para Codex en `.agents/skills/`. Utiliza en orden `$speckit-constitution`, `$speckit-specify`, `$speckit-clarify` cuando sea necesario, `$speckit-plan`, `$speckit-tasks`, `$speckit-analyze`, `$speckit-implement` y `$speckit-converge`. Si no están cargadas, comprueba su disponibilidad e instalación antes de improvisar; como contingencia puedes crear los artefactos equivalentes en las rutas de Spec Kit siguiendo sus plantillas, dejando constancia explícita de la limitación. No finjas que se ejecutó una habilidad que no se ejecutó.
4. Prioriza los requisitos de la asignatura: constitución, especificación funcional con Non-Goals, plan, tareas, app ejecutable, calidad técnica, tests ejecutados, README, Git colaborativo y demo.

**Producto a entregar:**
Una sola aplicación web EcoGest 360 con cinco features MVP: (1) usuarios, roles, institución piloto y catálogo; (2) registro y caracterización de residuos en kg con origen de dato; (3) lotes, saldos, QR y trazabilidad; (4) compostaje y resultados independientes; (5) dashboard y CSV. El recorrido de demostración completo debe ser generación de 25 kg *simulados* de orgánicos, creación de lote, transferencia de 20 kg a compostaje, bloqueo de transferencia adicional de 6 kg, registro de resultado de compost independiente, y reporte que no duplique masas ni haga pasar datos simulados por medidos. Verifica también permisos del rol consultor y sesiones no autenticadas.

**Arquitectura preferida (defínela formalmente en plan técnico):**
- `frontend`: React + Vite + TypeScript; UI moderna, sobria, responsive, en español, con accesibilidad básica y gráficos.
- `backend`: Python + Django 5.2 LTS + Django REST Framework; tests y controles en backend.
- Base de datos PostgreSQL con ORM y migraciones; opción de Docker Compose si ya funciona en el equipo. No cambies a otra base silenciosamente.
- `.env.example` y `.gitignore` seguros; cero claves reales y cero datos ambientales inventados.

**Ritmo de entrega**
- Primero define artefactos SDD coherentes, con cinco funcionalidades y Non-Goals. No pongas endpoints/tablas en `spec.md`; eso va en plan.
- Después implementa el circuito vertical con persistencia real y transacciones de saldos, permisos y pruebas. No implementes extras hasta que el MVP pase.
- Ejecuta comandos de instalación, arranque y pruebas realmente; registra los comandos y sus resultados en `docs/PRUEBAS.md`, con pendientes conocidos.
- El README debe permitir replicar la demo en Windows PowerShell sin depender de rutas privadas. Proporciona datos de prueba marcados *simulados*.
- No te limites a decir que terminaste: muestra evidencia, errores y limitaciones. Si se requiere una decisión crítica faltante, elige no ampliar riesgo/permisos, registra conflicto y continúa únicamente en tareas independientes seguras.

**GitHub y dos cuentas**
- Planea tareas para dos colaboradores reales: `Danilo2334` y `francisco3788`. Propón división auténtica de entregables/revisión (por ejemplo backend/QA y frontend/documentación). Respeta quién efectivamente trabajó y revisó cada cambio; nunca simules autoría ni una revisión inexistente.
- Antes de operar Git remoto inspecciona `git status`, `git remote -v`, `gh auth status` y `gh api user --jq .login`. No uses `Camm001E` para este proyecto.
- Si hay repo remoto autorizado, organiza ramas de tareas y commits descriptivos asociados a trabajo real; el dueño de cada cuenta debe revisar y autorizar sus commits/PR. Identidad Git por commit y autenticación `gh` son cosas diferentes. No publiques ni fusiones PR sin mi autorización expresa.
- No dejes todo Git para el último minuto: conserva puntos de recuperación y propone commits por hito.

**Límites**
- No gastar dinero, no instalar servicios pagos, no desplegar públicamente, no ejecutar comandos destructivos, no forzar push, no borrar datos, no publicar secretos ni alterar otros proyectos.
- No implementar IA con Gemini/chatbot/fotos ni un sistema agrícola completo en este MVP: su diseño quedará preparado como fase futura, pero la construcción y las pruebas reales tienen prioridad.
- No afirmar que un resultado está listo sin verificarlo. Si no se logra un componente, marcarlo de forma transparente como no implementado.

**Informe final:** tabla `feature | estado real | prueba ejecutada | resultado`; archivos SDD creados, qué cambió, comandos para ejecutar, estado de Git, brechas pendientes, demo paso a paso y siguientes tareas priorizadas. Empieza ahora con el diagnóstico del repositorio y los artefactos SDD; luego continúa en las tareas MVP autorizadas.

# EcoGest 360 — Plan de ejecución para una ventana de aproximadamente cinco horas

> Distribución orientativa, NO garantía. El agente debe privilegiar un flujo real demostrado sobre complejidad incompleta. El estudiante conserva control de permisos, aceptación y Git remoto.

| Prioridad | Bloque orientativo | Resultado verificable |
|---|---|---|
| 1 | Inicio / primer tramo | Auditoría de repo y entorno; constitución, spec y Non-Goals; decisiones relevantes resueltas; plan + tareas verificables |
| 2 | Tramo siguiente | PostgreSQL, backend Django, migraciones, roles, modelos centrales y validaciones de masa; tests base |
| 3 | Tramo central | React + UI responsive; flujo generación → lote → movimiento → compostaje; reportes e indicadores |
| 4 | Tramo de validación | Pruebas ejecutadas, fallos y correcciones, `README.md`, `.env.example`, datos demo simulados y comandos de arranque |
| 5 | Tramo final | Convergencia SDD, revisión Git, commits por contribución real, ramas/PR autorizados y demo con flujo principal |

## Evidencias obligatorias de la asignatura
1. Constitución en `.specify/memory/constitution.md` y SDD espec/plan/tareas versionados.
2. App ejecutable con ruta de instalación documentada y funcionamiento verificado.
3. Pruebas reales con comandos y salidas; QA negativos sobre cantidades/permisos.
4. README, instrucciones de configuración, variables de ejemplo y capturas o pasos de demo.
5. Git con cambios asociados a tareas concretas, ramas, commits descriptivos, PRs revisables y atribuciones verdaderas a cada integrante.
6. Registro de limitaciones técnicas y pendientes.

## Gestión de identidades y contribuciones
`gh auth status` lista las cuentas. `gh auth switch -h github.com -u <cuenta>` cambia la autenticación de GitHub CLI; `gh api user --jq .login` la comprueba. **Importante:** esta cuenta activa NO define por sí sola el autor del commit. `git config --local user.name` y `git config --local user.email` fijan identidad de commits; sólo usar datos propios y correos verificados/autorizados por cada colaborador. No reatribuir código de una persona para aparentar colaboración. No forzar push ni fusionar PRs sin revisión humana.

## Checklist final
- [ ] 5 features definidas y acotadas con Non-Goals
- [ ] Especificaciones/plán/tareas coherentes y `analyze`/`converge` documentados
- [ ] Aplicación arranca y soporta flujo principal en pantalla
- [ ] No movimientos > saldo, cero/negativo ni acceso sin permisos
- [ ] Indicadores no mezclan datos simulados con mediciones reales
- [ ] Pruebas ejecutadas y registro legible
- [ ] README y `.env.example` seguros
- [ ] Repositorio con commits/PR auténticos y responsables identificados

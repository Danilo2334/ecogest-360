## Alcance del MVP

Cinco áreas funcionales:
1. Gestión institucional, usuarios, roles y clasificación ambiental.
2. Registro y caracterización de residuos sólidos.
3. Recolección, movimientos, lotes y trazabilidad mediante QR.
4. Aprovechamiento, compostaje y economía circular.
5. Indicadores ambientales, dashboard e informes CSV.

Artefactos SDD: `.specify/memory/constitution.md` (1.1.0 ratificada) y
`specs/001-ecogest-mvp/spec.md`, `plan.md` y `tasks.md`.

El MVP registra residuos y conserva su trazabilidad desde generación y lotes hasta compostaje,
validación e indicadores. Las operaciones controlan saldo, permisos e idempotencia con PostgreSQL.
La auditoría corrige evidencia nula, adjuntos inválidos y fecha local; el cierre impide acreditar
procesos estimados. La constitución 1.1.0 autoriza SVG nativo accesible.

Validación local registrada: 30 pruebas Django, 5 Vitest y 3 Playwright aprobadas; TypeScript,
build y comprobación de migraciones correctos. Resultados y fallos iniciales en docs/PRUEBAS.md.

Pendientes: CHK013 humano, catálogo institucional real y ensayo de instalación independiente.
T008, T014, T019, T026 y T032 siguen parcialmente cumplidas por falta de evidencia TDD histórica. Sin paginación
ni lectura QR por cámara; no son nuevas funciones exigidas para esta entrega. Demo solo simulada.

| Commit | Autor registrado | Aportación declarada por el usuario |
| --- | --- | --- |
| `58bab1f` | Danilo Carlosama / Danilo2334 | Documentación SDD |
| `fd90a7d` | Danilo Carlosama / Danilo2334 | Backend y pruebas |
| `d680fb3` | Francisco Javier Molina Calderon / francisco3788 | Frontend y flujo completo |
| `d29b01b` | Francisco Javier Molina Calderon / francisco3788 | Correcciones, regresiones y cierre documental |

Los metadatos coinciden con la aclaración del usuario sobre el trabajo de cada integrante.
No prueban por sí solos quién realizó el trabajo ni constituyen una revisión independiente.
Ambos integrantes deben confirmar sus aportes desde sus cuentas reales. La revisión colaborativa sigue pendiente; abrir este PR no la completa. No se modificaron autores, fechas ni historial durante esta preparación.

Este PR se presenta en Draft. No autoriza merge ni despliegue.
El commit documental adicional corresponde a Danilo y conserva los cuatro commits anteriores.

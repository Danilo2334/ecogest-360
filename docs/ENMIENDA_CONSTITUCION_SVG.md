# Enmienda constitucional ratificada — SVG nativo

**Estado: APROBADA Y RATIFICADA por instrucción explícita del usuario.**
Versión anterior: 1.0.0. Versión vigente: **1.1.0**.
Fecha de propuesta y ratificación: **2026-11-15**. Cambio incorporado a la constitución.
Se conserva abajo la comparación presentada para aprobación.

## Cambio mínimo propuesto en §2, Frontend / UI

Texto anterior (1.0.0):

> Elegir y documentar una sola biblioteca de gráficos para evitar duplicidades.

Texto aprobado (1.1.0):

> Para los gráficos del MVP se permite SVG nativo accesible, con alternativa textual o tabular,
> sin biblioteca adicional. Si se aprueba una biblioteca de gráficos en una fase posterior,
> se elegirá y documentará una sola, evitando duplicidades y manteniendo accesibilidad.

El resto del apartado, los seis apartados principales, su lista de verificación y las reglas
ambientales, de seguridad y SDD se conservan sin cambios.

## Versión e impacto

Se adopta MINOR 1.1.0 porque amplía expresamente las alternativas técnicas permitidas;
no se presenta como corrección tipográfica PATCH. No cambia APIs, datos, permisos ni fórmulas.
Las implementaciones con una biblioteca única seguirían siendo compatibles. La selección
de versión fue aprobada expresamente por el usuario.

Motivo: reconciliar la constitución con research.md, T035 y ReportsPage.tsx, que ya utilizan
SVG y tabla accesible. Instalar Recharts/Chart.js solo por la redacción no añade una capacidad
aprobada del producto. No se instalaron bibliotecas ni se modificó el gráfico con esta propuesta.

## Impacto de sincronización al aprobar

- `.specify/memory/constitution.md`: sustituir únicamente la oración indicada, actualizar
  versión/fecha de enmienda y registrar aprobación conservando la fecha original de ratificación.
- `plan.md` y `docs/DECISIONES.md`: sustituir estado pendiente por referencia a la versión ratificada.
- `docs/AUDITORIA_FINAL.md`: cerrar la discrepancia documental solo después de aprobación.
- `spec.md`, modelos y migraciones: sin cambios necesarios por esta enmienda.
- Plantillas originales de la profesora: no modificar.

Evidencia existente: frontend/src/features/reports/ReportsPage.tsx, frontend/tests/reports.test.tsx,
recorridos Playwright y capturas del dashboard. No implica certificación WCAG.

## Registro de decisión humana

- Decisión: aprobar y ratificar la enmienda SVG.
- Persona que aprueba: usuario responsable del proyecto, mediante instrucción explícita en este chat.
- Fecha de aprobación: 2026-11-15.
- Versión finalmente aprobada: 1.1.0.

La constitución vigente es 1.1.0. Se cierra la discrepancia SVG por aprobación explícita,
sin instalar dependencias ni modificar las reglas de dominio. Esto no aprueba CHK013.

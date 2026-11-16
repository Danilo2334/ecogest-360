# Investigación de diseño — 2026-11-16

Inspección local y revisión delegada requerida por speckit-plan; no llamadas de pago.

- Decisión: componer report() V1 con corte congelado. Razón: fuente existente de G/A y reglas
  CHK004; alternativa rechazada: calcular acreditación en navegador o sumar Output.
- Decisión: comparación de períodos completos contiguos con igual duración y filtros.
  Razón: no comparar períodos parciales; todavía difieren en maduración y cobertura.
- Decisión: series agrupadas por fecha local, ranking por area_id+nombre. Días ausentes son
  ausencia de registro. Razón: nombre no es identidad; cero registro no prueba cero residuos.
- Decisión: endpoint GET nuevo, whitelist explícita; no tocar forma de listas ni dashboard V1.
- Decisión: SVG nativo y CSS Modules, componentes tipados y carga selectiva. Sin dependencias nuevas.
- Decisión: planes futuros con esquema aditivo; simulación no persistente y asistente sin escritura.
- Integración OpenAI investigada previamente en decisiones-y-compatibilidad.md con fuentes oficiales;
  se difiere SDK/modelo/gasto a E. El servicio permanece ausente/apagado durante A.
- No hay bloqueantes de A. PDF docente Brownfield ausente; metodología aportada por equipo aplicada.

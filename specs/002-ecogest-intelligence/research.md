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
# Decisión de implementación E (2026-11-16)

SDK oficial openai 3.51.0; Responses API con esquema estricto. Modelo configurable
OPENAI_MODEL=gpt-5.6-terra, sin sustitución automática. El catálogo oficial consultado
ya marca gpt-4.1-mini, gpt-5-mini y gpt-5.4-nano deprecados. Terra permite reasoning none
y salida estructurada; se propone por vigencia y alcance acotado, no se probó su latencia
ni disponibilidad en esta cuenta. Tarifa consultada USD 2 entrada / 12 salida por millón;
reserva conservadora usa 2.5 entrada para cubrir cache-write y 12 salida. Revalidar antes
de activar. Presupuesto NO aprobado; ninguna llamada real autorizada o ejecutada.

Fuentes primarias: [modelo y tarifa](https://developers.openai.com/api/docs/models/gpt-5.6-terra),
[SDK](https://github.com/openai/openai-python),
[Responses estructurada](https://developers.openai.com/api/docs/guides/structured-outputs),
[retención](https://developers.openai.com/api/docs/guides/your-data).
store=false evita conservar estado recuperable de Responses, no promete retención cero del
proveedor. Las tres modalidades seleccionan evidencias y explicaciones locales verificables;
la restricción a catálogo evita validar texto libre con heurísticas insuficientes. La IA
clasifica intención y relevancia; no calcula cifras, ni ejecuta acciones. Conversación solo
en memoria de pantalla, se elimina al salir/cerrar sesión; cambiar filtros identifica la respuesta anterior.

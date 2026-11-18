# Inventario de entrega académica

Actualización V2 al final; la tabla siguiente conserva el antecedente de preparación V1.

Preparación local; no significa publicación, aprobación humana ni carga en Campus UCC.

| Contenido | Ubicación | Estado |
| --- | --- | --- |
| Constitución vigente y enmienda | .specify/memory/constitution.md; docs/entrega/ENMIENDA_CONSTITUCION_SVG.md | 1.1.0 ratificada; retirar comentario temporal de revisión antes del commit |
| Especificación, plan, tareas y contratos | specs/001-ecogest-mvp/ | Disponibles; cinco tareas TDD conservan estado parcial |
| Código y migraciones reproducibles | backend/; frontend/src/; compose.yaml | Implementados; incluir requirements y package-lock |
| Instalación y configuración segura | README.md; .env.example; scripts/ | Disponibles; nunca incluir .env real |
| Pruebas y resultados | backend/tests/; frontend/tests/; docs/PRUEBAS.md | Última ejecución 38 aprobadas; no reejecutadas en preparación Git |
| Decisiones, auditoría y matriz docente | docs/DECISIONES.md; docs/entrega/AUDITORIA_FINAL.md; docs/entrega/MATRIZ_CUMPLIMIENTO_DOCENTE.md | Disponibles; PDF oficial aún fuera del repositorio |
| Capturas de demostración simulada | docs/evidencias/ | Disponibles; no sustituyen ejecución humana |
| Guion y registro humano | docs/entrega/DEMO_ACADEMICA.md; docs/entrega/REGISTRO_DEMO_HUMANA.md | Guion disponible; registro vacío y CHK013 pendiente |
| Preparación del PR y cambios locales | docs/historico/PREPARACION_GITHUB.md; docs/historico/PR_MVP_PROPUESTO.md; docs/historico/RESUMEN_CAMBIOS_PARA_COMMIT.md | Propuestos; no ejecutados |
| Aporte de Francisco y revisión | `d680fb3`, `d29b01b`; procedimiento en docs/historico/PREPARACION_GITHUB.md | Autoría según aclaración del usuario; confirmación personal, PR y revisión pendientes. Ensayo de instalación adicional aún no ejecutado |
| Enlaces de repositorio privado, PRs y revisiones | Por registrar tras autorización y ejecución | Pendientes |
| Entrega individual de ambos integrantes | Campus UCC; constancia individual | Pendiente; no sustituida por GitHub |

Excluir credenciales, datos privados, entorno virtual, dependencias instaladas, compilaciones,
archivos media y capturas de errores que puedan contener información sensible. Versionar solo
capturas revisadas con datos simulados. No fabricar videos, firmas ni constancias de participación.

Preparación visual: se abrió la pantalla de acceso de EcoGest 360 en Chrome mediante control
del agente. Esto acredita disponibilidad de la pantalla, no una demo humana ni cierre de CHK013.


## Actualización local V2 — 2026-11-16

- Constitución 1.1.0 y artefactos V1 preservados; fuentes V2 en specs/002-ecogest-intelligence.
- A–E implementadas. Resultado vigente de pruebas en docs/PRUEBAS.md (69 backend, recorridos
  completos y específicos, Vitest y build). La cifra 38 de la tabla es histórica.
- Capturas actuales revisadas: docs/evidencias/v2/integracion y docs/evidencias/v2/asistente.
  Originales de fases preservados; README enlaza fuentes canónicas y antecedentes.
- Guion audiovisual V2 reutiliza docs/entrega/DEMO_ACADEMICA.md; CHK013 sigue pendiente, sin firmas fabricadas.
- Asistente OpenAI apagado tras dos consultas reales autorizadas desde Django el 2026-11-16:
  presupuesto USD 0,12 y costo local calculado USD 0,00538700. Véase
  [registro de pruebas](../PRUEBAS.md). Flujo completo del navegador con OpenAI real,
  saldo y facturación oficial no verificados; no autoriza nuevas llamadas.
- V2 solo local. Historial previo, main, rama MVP y respaldo preservados; no publicación/merge.
- Revisión auténtica por ambos integrantes y carga individual en Campus UCC pendientes.

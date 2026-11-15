# Calidad de requisitos: integridad ambiental y permisos

**Purpose**: Revisión previa a implementación, profundidad estándar centrada en masas y acceso.
**Created**: 2026-11-15
**Feature**: [spec.md](../spec.md)
**Review Ownership**: El revisor marca cada criterio tras comprobar calidad de requisitos.
**Marker Semantics**: [x] significa requisito revisado, no funcionalidad implementada.

## Completitud y claridad

- [ ] CHK001 ¿La matriz diferencia confirmación ordinaria y validación ambiental sin herencia implícita? [Clarity, Spec §Clarifications, FR-005]
- [ ] CHK002 ¿Las reglas distinguen disponible, asignado, consumido, generado y acreditado? [Clarity, Spec §FR-013, FR-021–022]
- [ ] CHK003 ¿La corrección permitida y la incidencia histórica están delimitadas sin reversiones implícitas? [Completeness, Spec §FR-009, Clarifications]
- [ ] CHK004 ¿La evidencia de destino y las condiciones de confirmación están descritas de forma verificable? [Completeness, Spec §FR-019]

## Consistencia y escenarios

- [ ] CHK005 ¿La masa de salida permanece separada de la masa de entrada en todos los indicadores? [Consistency, Spec §FR-018–021]
- [ ] CHK006 ¿Los casos de concurrencia, reenvío y fallo parcial tienen resultados inequívocos? [Coverage, Spec §User Story 3, Edge Cases]
- [ ] CHK007 ¿La procedencia simulada se conserva también en evidencia y validación de demostración? [Consistency, Spec §Clarifications]
- [ ] CHK008 ¿Los requisitos de cohorte, corte y correcciones vigentes aclaran límites históricos? [Clarity, Spec §Clarifications, FR-021]

## Medición, dependencias y límites

- [ ] CHK009 ¿Los escenarios 25/20/8 y denominador cero permiten evaluar cifras esperadas sin supuestos? [Measurability, Spec §Clarifications, User Story 5]
- [ ] CHK010 ¿La selección del catálogo piloto está identificada como dependencia y no como catálogo oficial inventado? [Dependency, Spec §Assumptions]
- [ ] CHK011 ¿El alcance de acreditación de entregas externas está suficientemente acordado? [Assumption, Spec §FR-022, Non-Goals]
- [ ] CHK012 ¿Los requisitos de acceso abarcan QR, evidencias y exportaciones además de pantallas? [Coverage, Spec §FR-003, FR-011, FR-024]
- [ ] CHK013 ¿Los criterios de teclado, errores y tamaños de pantalla son medibles? [Measurability, Spec §FR-025, SC-006]

## Notes

13 criterios nuevos, pendientes de revisión; no se adjudica aprobación humana.
speckit-implement lee estos marcadores, pero no los modifica.

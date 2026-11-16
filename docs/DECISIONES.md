# Decisiones de EcoGest 360

## 2026-11-15 — Aclaración y diseño SDD

- Usuario aprueba Q1 B: operador confirma operaciones ordinarias; gestor valida aprovechamiento.
- Usuario aprueba Q2 A: bloquear modificación de masas consumidas y lotes cerrados;
  incidencias históricas pendientes sin alterar historial; correcciones permitidas auditadas.
- Usuario aprueba Q3 A: acreditar entradas de compostaje solo al finalizar y verificar
  proceso, salida independiente, fecha, responsable y destino. No sumar entrada y salida.
- Constitución 1.0.0 ratificada se conserva sin cambios en esta etapa.
- Diseño: sesiones CSRF, PostgreSQL real, Decimal, bloqueos e idempotencia; fuentes y alternativas
  en specs/001-ecogest-mvp/research.md. Estas son decisiones de diseño para revisión.
- Supuestos por revisar antes de implementación: acreditación limitada a compostaje y
  corrección de generación solo sin asignaciones, según checklists/requirements.md.
- Skill checklist requiere plan existente en esta instalación: primer intento informó ausencia
  de plan; se preparó con setup-plan y luego la resolución de checklist fue correcta.
- Git permanece en main; el BRANCH del resolver representa el identificador de feature,
  no evidencia de creación de una rama. No hay commits ni autores asignados.

Próximo hito: revisar diseño, supuestos y lista de calidad; autorizar implementación y,
por separado, el primer commit documental. No se interpretan estos pendientes como autorización.

## Autorización de implementación 2026-11-15
A1 y A2 aprobados expresamente. Dashboard distinguirá compostaje acreditado del total institucional y de entregas externas. Se autorizan implementación, instalaciones aisladas, base nueva y commits locales con identidad verificada. Los 13 criterios de revisión se conservan abiertos; el usuario autoriza continuar. Identidad Git y cuenta activa verificadas: Danilo2334, id 134672640.


## Decisiones de implementación

- PostgreSQL 16 en contenedor dedicado ecogest360, volumen nuevo y puerto loopback 55436.
  Usuario de aplicación ecogest_app sin superusuario; CREATEDB exclusivamente para tests locales.
- Frontend en 5178 porque 5173 estaba ocupado; no se detuvo el proceso ajeno.
- Los servicios de dominio permanecen separados; el transporte REST se concentra en core/views.py.
  Movement de tipo entrega/entrada_compostaje representa el consumo único, evitando una entidad
  Consumption duplicada; ConsumptionSource conserva reparto por origen. No cambia regla de masa.
- Idempotencia: bloqueo transaccional advisory por institución/actor/ruta/clave antes de consultar
  el recibo único; evita carreras de reintentos sin continuar transacciones rotas.
- CSS Modules compartidos y pantallas separadas bajo frontend/src/features/. No se agregó biblioteca
  de gráficos; SVG accesible y tabla representan datos reales de la consulta.
- Para el piloto, las listas devuelven arrays; no se implementó la paginación prevista en el
  contrato inicial. El panel agrega directamente en PostgreSQL y CSV prepara filas solo al exportar.
  La carga es selectiva por pantalla; paginación permanece como mejora para listados voluminosos.
- La fase inicial roja se ejecutó con el flujo vertical antes de existir los módulos. Varias pruebas
  especializadas se añadieron después: no se atribuye una secuencia TDD completa a cada tarea.

## Auditoría posterior — 2026-11-15

- Se conservaron constitución, tres commits y autoría. Sin staging, commits ni publicación.
- Correcciones dentro del alcance: rechazar textos obligatorios nulos y adjuntos inesperados;
  fecha inicial del formulario en hora local, no recorte UTC. Pruebas de regresión ejecutadas.
- Se informa contradicción SVG/biblioteca de gráficos y regla de salida estimada/medición propia
  sin enmendar constitución ni decidir reglas ambientales nuevas. Ver AUDITORIA_FINAL.md.
- No se agrega paginación durante auditoría: no la exige spec.md, aunque rendimiento de todos
  los listados a 10 000 registros no está demostrado. Panel/CSV sí tienen medición local.
- Aprobaciones humanas y cinco tareas TDD históricas permanecen pendientes; nuevas pruebas
  no sustituyen ni retrofechan evidencia del desarrollo inicial.

## Cierre de CHK004 autorizado

El usuario aprueba acreditar únicamente procesos medidos con entrada y salida medida propia,
evidencia verificable y validación del gestor; simulados solo en su universo de demostración.
Procesos estimados no se confirman ni aportan A. Regularización fuera del MVP. No se cambia
procedencia, masa o evidencia silenciosamente. Confirmaciones estimadas históricas, si existen,
permanecen en el historial pero quedan excluidas del indicador bajo la nueva regla.
Primero se actualiza spec.md; después se ejecutan regresiones rojas y se aplica corrección mínima.
No se autoriza ratificar automáticamente la enmienda SVG: se prepara propuesta separada.

## Criterios docentes confirmados por transcripción del usuario

La matriz académica adopta los seis títulos exactos que el usuario comunica del PDF docente,
página 2, consultado externamente. El PDF sigue fuera del repositorio y no fue inspeccionado
directamente por el agente. Se reemplaza la clasificación provisional, sin notas ni porcentajes.
Se incorpora la obligación comunicada de página 8: entrega individual de cada integrante en
Campus UCC, aún pendiente. No implica autorización de publicación, carga, push ni merge.
Este ajuste es documental; conserva resultados de pruebas, cinco tareas TDD parciales,
CHK013 pendiente y propuesta SVG sin ratificar. CHK004 ya está corregido y probado.

## Ratificación SVG — 2026-11-15

Por autorización explícita del usuario se ratifica constitución 1.1.0 con fecha 2026-11-15.
Solo se amplía §2 para permitir SVG nativo accesible con tabla/texto alternativo, evitando
dependencia innecesaria. Se preservan seis apartados docentes y todas las reglas restantes.
El resolvedor de Spec Kit funciona; se mantiene estructura docente por instrucción del usuario
frente a la plantilla genérica resuelta. No hay hooks de extensiones configurados.
Los estados anteriores de «propuesta pendiente» son históricos; el vigente es ratificado.
No se crean commits ni remotos: únicamente propuesta de cierre, PR y aporte independiente.

## Cierre local autorizado

El usuario autoriza el commit local de correcciones, pruebas, documentación y evidencias del
MVP con identidad real de Danilo. Se conserva el historial previo, sin fechas ni autores
reescritos. Se retira únicamente el comentario temporal de revisión de la constitución.
El PDF fue compartido/revisado en la conversación según la aclaración recibida; falta su copia
local. No se atribuye consulta personal al estudiante ni lectura directa al agente local.
CHK013 y cinco tareas TDD siguen pendientes; última ejecución de software: 38 aprobadas.
Este cierre no repite auditorías ni pruebas y no autoriza repositorio remoto, push o merge.

## Conciliación documental de autoría y preparación de GitHub — 2026-11-15

| Commit | Autor registrado | Aportación declarada por el usuario |
| --- | --- | --- |
| `58bab1f` | Danilo Carlosama / Danilo2334 | Documentación SDD |
| `fd90a7d` | Danilo Carlosama / Danilo2334 | Backend y pruebas |
| `d680fb3` | Francisco Javier Molina Calderon / francisco3788 | Frontend y flujo completo |
| `d29b01b` | Francisco Javier Molina Calderon / francisco3788 | Correcciones, regresiones y cierre documental |

Los metadatos coinciden con la aclaración del usuario sobre el trabajo de cada integrante.
No prueban por sí solos quién realizó el trabajo ni constituyen una revisión independiente.
Ambos integrantes deben confirmar sus aportes desde sus cuentas reales. Las revisiones y PRs
siguen pendientes. No se modificaron autores, fechas ni historial durante esta preparación.

Se conservan main y la base común en `58bab1f`, implementación en `d29b01b` y respaldo
solo local. Las declaraciones previas sobre autor único corresponden al estado anterior
a la aclaración del usuario. CHK013 y cinco tareas TDD parciales no cambian.

## 2026-11-16 — Intelligence: aprobación y fase A

Usuario aprueba Q1 períodos completos comparables, Q2 simulador efímero/planes persistentes
solo gestor y Q3 IA contextual opcional sin escritura ni gasto hasta autorización. Solo fase A
implementada: identidad/navegación/Observatorio; sin nuevas dependencias o migraciones.
Se conserva report() V1 como fuente de G/A. Consulta observatory aditiva, corte compartido,
comparación no disponible ante evidencia insuficiente, procedencias separadas y fechas Bogotá.
Plan/tareas/contratos en specs/002-ecogest-intelligence; informe y capturas en INFORME_FASE_A_V2.md.
No commits, push, merge, despliegue o modificaciones del PR #1. Backend de desarrollo reiniciado
por usar --noreload; datos conservados. B–F requieren nueva autorización.


## 2026-11-16 — Refinamiento A autorizado

Se conserva identidad verde/marfil. Balance G=A+pendiente, distribución por material y
hallazgos deterministas; KPI consultan cohorte base sin confundirla con masa acreditada.
Escenario SIMULADO opcional en institución separada, comando explícito probado antes de
ejecutar, sin restablecimientos. Fechas explicativas es-CO y controles nativos conservados.
Filtros plegables en móvil; detalle metodológico accesible. No se inicia Pasaporte ni IA.
Ver docs/INFORME_REFINAMIENTO_OBSERVATORIO.md y docs/DATOS_DEMO_OBSERVATORIO.md.


## 2026-11-16 — Orden final V2: ejecución local B–E

Usuario autoriza completar B–E, integración, migraciones aditivas y commits locales auténticos.
Sin push, merge ni gasto IA. Checkpoint del Observatorio: b082971, autor configurado Danilo
Carlosama (correo noreply Danilo2334), sin alterar contribuciones anteriores. Revisión de
candidatos sin patrones de secretos; .env excluido. OPENAI_API_KEY presente (solo booleano).
Checklist documental 17/17; no hooks de extensión. Documentos con autorizaciones anteriores
se conservan como historia; spec/plan/tasks incorporan orden vigente.
Pasaporte construido como proyección institucional: autor de creación de lote no persistido
se muestra no disponible, controles usan su fecha registrada y salida compartida pertenece al
proceso completo. No nuevos modelos ni escrituras ambientales en B.


### Simulación y preparación de persistencia D

C usa cálculo Decimal sobre report V1: E descuenta consumos por origen (no asignaciones
dos veces), N toma solo categoría negro, token de base excluye corte volátil pero incluye
fuentes/valores/consumos/filtros. Corte histórico se rechaza. Escenarios no persistentes.
Respaldo previo a Planes en backups/ecogest-before-v2-plans-20261116.dump, excluido de Git,
119353 bytes; pg_restore --list legible y restauración exitosa en base independiente
ecogest_v2_migration_trial_20261116. Aún no se aplicaron migraciones nuevas.

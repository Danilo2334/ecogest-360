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

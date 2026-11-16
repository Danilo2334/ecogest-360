# Contratos de aplicación propuestos

Base `/api/`. JSON UTF-8; masas como cadenas decimales en kg, fechas ISO 8601 con zona.
No es implementación. Referencias a [modelo](../data-model.md) y [especificación](../spec.md).

## Convenciones comunes

Sesión de usuario y CSRF en todas las mutaciones, incluido login. 401 sin sesión con
WWW-Authenticate, 403 sin permiso o CSRF, 404 recurso inexistente/no visible, 400 entrada inválida,
409 saldo/estado/reintento incompatible. Error: code, message en español, field_errors opcional.
Implementación del piloto: listas como arrays sin paginación. Paginación queda como mejora técnica; no cambia filtros ni permisos.
El servidor deriva institución/actor de membresía; no confía en campos enviados por cliente.
Idempotency-Key obligatorio en creación de generación, lote, movimiento, entrada, finalización,
confirmación y cierre; UUID de operación retenido por cliente mientras desconoce resultado.
Misma clave y contenido repite resultado; contenido distinto devuelve 409. Reintento no vuelve
a enviar un consumo nuevo. Decimales excesivos se rechazan; no convertir a float.

| Método y ruta | Rol | Entrada / salida principal |
| --- | --- | --- |
| GET session/csrf | Anónimo | Token CSRF sin datos privados |
| POST session/login | Anónimo con CSRF | Identificador y contraseña / usuario, rol; nunca registrar contraseña |
| POST session/logout | Autenticado | Revocar sesión |
| GET session/me | Autenticado | Usuario y membresía |
| GET institution, sites, areas, materials, users | Autenticado; users solo administrador | Datos autorizados |
| POST/PATCH sites, areas, materials, users | Administrador | Alta/actualización; cambios de rol auditados; no autoconceder rol superior |
| PATCH institution | Administrador | Datos del único piloto, sin alta multiinstitución |
| GET/POST generations | Lectura todos; escritura operador | Fecha, área, material, kg, procedencia, método / registro confirmado |
| GET generations/{id} | Autenticado | Detalle, asignaciones e historial |
| POST generations/{id}/review | Gestor | Validar clasificación / revisión, sin crear masa |
| POST generations/{id}/correct | Gestor | Campos permitidos y motivo / registro y auditoría; 409 si asignado |
| GET/POST lots | Lectura todos; escritura operador | Fuentes y kg / ID, QR autenticado, saldo |
| GET lots/{uuid} | Autenticado | Orígenes, eventos, saldo y estado |
| POST lots/{id}/movements | Operador | Tipo logístico o entrega, kg, fecha, destino; efecto único |
| POST lots/{id}/close | Operador | Cierre si agotado y sin proceso abierto |
| GET/POST compost/processes | Lectura todos; escritura operador | Inicio y procedencia / proceso |
| POST compost/processes/{id}/inputs | Operador | Lote, kg, fecha / entrada + movimiento + consumo únicos |
| POST compost/processes/{id}/measurements | Operador | Tipo, valor, unidad, fecha |
| POST compost/processes/{id}/finalize | Operador | Salida kg, fecha, destino, procedencia / finalizado pendiente |
| POST compost/processes/{id}/evidence | Operador o gestor | Documento o referencia, receptor, fecha y descripción |
| GET evidence/{id}/download | Autenticado autorizado | Descarga privada, nunca URL pública directa |
| POST compost/processes/{id}/verify | Gestor | Confirmar o rechazar, motivo / validación auditada |
| GET/POST incidents | Lectura todos; escritura operador, gestor o administrador | Referencia y motivo / pendiente sin cambiar entidad |
| GET dashboard | Autenticado | G, A, disponible, en proceso, pendiente, tasa y contexto |
| GET reports/generation.csv | Autenticado | Filas filtradas + metadatos coherentes con panel |

## Reportes

CHK004: POST verify con decisión confirmado devuelve 400 para procesos estimados o salida
de procedencia incompatible, sin crear Verification ni modificar masa/procedencia. Medidos
requieren salida medida independiente y evidencia; simulados se confirman solo como demo.
El panel/CSV excluye de A las confirmaciones estimadas históricas, conservando sus registros.

Filtros: generated_from, generated_to (inclusivos en zona del piloto), area, material,
provenance y cutoff. Validar fechas y procedencias; excluir eventos posteriores al corte del
numerador. Denominador usa generación vigente de cohorte, no suma movimientos.
Respuesta incluye fórmula, unidades, universo, corte, calidad, provisional y limitaciones.
CSV lleva columnas de contexto repetidas por fila, IDs de generación, masa generada y
acreditada por origen. Sin registros: una fila row_type=metadata conserva filtros/corte y ceros; no representa generación. Las filas ordinarias llevan row_type=generation.
Neutralizar textos que comiencen por =, +, -, @ o caracteres de control y escapar CSV.

## Contrato UI

Login; administración institucional; registro/listado/detalle; lotes y movimientos;
procesos, evidencia y validación; dashboard/exportación. Navegación por rol, errores de
campo y generales, estados de carga/vacío, foco visible y tabla alternativa al gráfico.
Una operación pendiente de red no se repite con nueva clave. Campos de masa mantienen texto
decimal. Mostrar siempre procedencia y separar «finalizado» de «verificado».
UI de incidencias accesible desde detalle, también cuando el lote está cerrado.

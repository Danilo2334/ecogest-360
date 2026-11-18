Actúa como un **analista de requisitos de software especializado en Spec-Driven Development (SDD)**.

Necesito que me ayudes a redactar las **especificaciones funcionales de un proyecto de software**, utilizando la siguiente información:

**Nombre del proyecto:** [Nombre del proyecto]

**Descripción:** [Explica brevemente qué problema resuelve, para quién está dirigido y cuál es su propósito principal].

**Funcionalidades que deseo implementar:**
[Describe las funcionalidades que consideras necesarias, aunque todavía no estén completamente definidas].

**Restricciones o reglas de negocio conocidas:**
[Indica las condiciones que el sistema debe cumplir. Si todavía no existen, escribe "Por definir"].

### Instrucciones para generar las especificaciones

1. Organiza el documento bajo el título `## Features principales`.
2. Divide las funcionalidades en módulos numerados, utilizando encabezados `### 1. Nombre del módulo`.
3. Para cada módulo, describe mediante viñetas qué debe permitir, mostrar, registrar o validar el sistema.
4. Identifica las reglas de negocio críticas y destácalas en **negrita**, especialmente aquellas relacionadas con validaciones, restricciones, integridad y trazabilidad.
5. Sugiere funcionalidades adicionales únicamente cuando sean indispensables para el funcionamiento del sistema, manteniendo un alcance académico manejable.
6. Agrega una sección titulada `## Lo que NO se va a construir en esta iteración (Non-Goals)`, indicando explícitamente las funcionalidades excluidas.
7. No incluyas código fuente, endpoints, modelos de base de datos, estructura de carpetas ni decisiones técnicas de implementación.
8. No inventes reglas de negocio críticas. Cuando falte información necesaria, señala el aspecto como pendiente de definición.
9. Utiliza un lenguaje claro, preciso y verificable, evitando requisitos ambiguos.
10. Prioriza una primera versión funcional (MVP), sin agregar características innecesarias.

### Formato de entrega

Genera un archivo **Markdown (`spec.md`)** que contenga únicamente las especificaciones funcionales y los Non-Goals.

El documento debe estar preparado para utilizarse como entrada del comando `/speckit.specify` de GitHub Spec Kit.

**Importante:** Si adjunto una constitución del proyecto, respeta sus reglas, restricciones y alcance. No agregues funcionalidades que contradigan dicha constitución.
# EcoGest 360 · paquete para Codex

## Aplicación segura al proyecto YA creado

1. Copia **`AGENTS.md`** y la carpeta **`docs/`** de este paquete a la carpeta del proyecto existente `C:\Users\molin\OPEN SPEN\document-management`. Mantén las carpetas `.specify/` y `.github/` existentes: no las reemplaces.
2. Abre esa carpeta raíz en VS Code o Codex.
3. En PowerShell verifica `codex --version`. Si no se reconoce, instala Codex CLI con el instalador oficial de Windows o npm; la extensión de VS Code por sí sola no siempre proporciona el comando de consola.
4. Dentro de la raíz del proyecto, ejecuta `specify integration install codex`, después `specify integration use codex`, y verifica `specify integration status`.
5. En Codex pega el contenido completo de `PROMPT_INICIO_CODEX.md` (no en PowerShell). Las habilidades Spec Kit se llaman con prefijo `$`, por ejemplo `$speckit-constitution`.
6. El nombre de carpeta `document-management` es heredado de la clase: el **producto** se denomina EcoGest 360. Podrás renombrar el repositorio después si conviene, sin borrar los artefactos.

## Importante
- Los documentos `01_...` y `02_...` son propuestas preexistentes; Codex debe alinearlos con el MVP definido en `03_...` y con la plantilla del docente.
- No copíes `PROMPT_INICIO_CODEX.md` dentro de `docs` si no quieres: basta leerlo y pegarlo en Codex.
- Dos cuentas GitHub no equivalen automáticamente a dos contribuciones verificadas. Cada persona debe revisar y hacerse cargo de su trabajo real.
- Entrega académica: artefactos SDD, app ejecutable, pruebas, README, Git y demo.

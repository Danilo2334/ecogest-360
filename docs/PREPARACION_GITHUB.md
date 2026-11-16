# Preparación de GitHub — comandos propuestos, NO ejecutados

Estado base: tres commits históricos más el cierre local autorizado; rama de implementación
feat/001-ecogest-mvp; main en 58bab1f. Consultar `git log -4 --oneline` para el hash del cierre.
Sin remoto. Este documento no autoriza crear repositorio, invitar colaboradores, subir ramas,
abrir PR ni fusionar. Ejecutar cada fase únicamente tras autorización correspondiente.
Sintaxis de creación de repositorio y PR contrastada con la ayuda de GitHub CLI instalada.

Verificación final de preparación: `gh auth status` reconoce Danilo2334 como cuenta activa
y francisco3788 como cuenta autenticada inactiva. No se cambiaron cuentas ni se comprobó
una contribución de Francisco por el mero hecho de que su sesión exista. Identidad Git:
Danilo Carlosama, correo noreply de Danilo2334. Tres commits conservados y sin remotos.
`.gitignore` excluye .env, venv, node_modules, dist y media; comparación de 155 archivos
candidatos con secretos locales sin coincidencias. Es una comprobación acotada, no certificación.
Inventario de entrega: CHECKLIST_ENTREGA.md.

## 1. Propuesta de commit de cierre

Mensaje: `fix: cerrar auditoria ambiental y ratificar constitucion 1.1.0`.
Autor: identidad real actual de Danilo Carlosama / Danilo2334, sin cambios de configuración.
Contenido: correcciones de auditoría y CHK004, regresiones, ratificación SVG, documentación
y evidencias simuladas revisadas. Ver RESUMEN_CAMBIOS_PARA_COMMIT.md y diff completo.
No atribuir este trabajo a Francisco. El comentario temporal Sync Impact Report se retiró
al preparar el cierre local; no altera la enmienda ratificada.

Comprobaciones previas desde raíz (lectura):

```powershell
git status --short --branch
git diff --check
git diff --stat
git config user.name
git config user.email
gh api user --jq .login
git remote -v
```

Revisar también archivos nuevos con `git ls-files --others --exclude-standard` y comparar
secretos sin imprimirlos. No usar `git add .` sin inspección. Seleccionar rutas revisadas,
inspeccionar `git diff --cached --stat` y `git diff --cached`, y solo entonces, con autorización:

```powershell
git commit -m "fix: cerrar auditoria ambiental y ratificar constitucion 1.1.0"
```

## 2. Repositorio privado y PR de integración, cuando se autorice

Nombre propuesto: Danilo2334/ecogest-360; confirmar disponibilidad/nombre antes de ejecutar.
No inicializar README/licencia remota para no crear una historia independiente.
Si origin ya existe, inspeccionarlo; no sobrescribirlo ni repetir creación.

```powershell
gh repo create Danilo2334/ecogest-360 --private --source . --remote origin
git remote -v
git push -u origin main
git push -u origin feat/001-ecogest-mvp
gh pr create --repo Danilo2334/ecogest-360 --base main --head feat/001-ecogest-mvp --draft --title "EcoGest 360: MVP ambiental y cierre de auditoria" --body-file docs/PR_MVP_PROPUESTO.md
```

Los push anteriores son acciones futuras sujetas a permiso; no se ejecutaron. El PR conserva
los commits existentes, muestra los cambios desde main y se revisa antes de cualquier merge.
No usar `gh pr create --dry-run` como garantía de ausencia de push: la ayuda local advierte
que puede subir cambios. No se propone comando automático de merge ni de despliegue.

Después de autorizar acceso, Danilo invita a francisco3788 al repositorio privado. Francisco
acepta con su propia cuenta. Nadie cambia cuentas para escribir en nombre del otro.

## 3. Contribución independiente propuesta para Francisco

**Tarea concreta:** reproducir el README en su propio entorno y elaborar
`docs/VERIFICACION_INSTALACION_FRANCISCO.md` con fecha real, versiones, pasos ejecutados,
resultados y dificultades; proponer las correcciones necesarias al README basadas en su ensayo.
No rellenar ese documento antes de que él lo haga. Aceptación: pasos reproducibles, resultados
reales, sin credenciales, sin afirmar aprobación donde hubo fallo, y una revisión de Danilo.
Esto es una aportación independiente de documentación/QA, no reasignación del código existente.

Opción para empezar antes del merge del MVP: Francisco parte de la rama de implementación y
abre su PR contra ella; se revisa su contribución primero, y luego el PR global hacia main.
Desde su equipo/cuenta, después de tener acceso y autorización:

```powershell
gh api user --jq .login
gh repo clone Danilo2334/ecogest-360
cd ecogest-360
git config user.name
git config user.email
git switch --create docs/francisco-reproduccion --track origin/feat/001-ecogest-mvp
# Francisco ejecuta el ensayo y redacta su informe real antes de continuar.
git add -- docs/VERIFICACION_INSTALACION_FRANCISCO.md
# Si corrigió README, añadirlo solo tras inspeccionar su diff.
git diff --cached
git commit -m "docs: registrar verificacion independiente de instalacion"
git push -u origin docs/francisco-reproduccion
gh pr create --repo Danilo2334/ecogest-360 --base feat/001-ecogest-mvp --head docs/francisco-reproduccion --title "Verificacion independiente de instalacion" --body-file docs/VERIFICACION_INSTALACION_FRANCISCO.md
```

Francisco debe verificar que login y autor configurado sean los suyos antes de crear su commit;
no se proporcionan datos inventados de nombre/correo. Sin `--author`, amend, force-push ni
reescritura del historial. La revisión y el merge requieren acciones reales y autorización.
Si el MVP ya fue integrado, partir de main actualizado y usar main como base del PR.

## 4. Evidencias finales y entrega

Conservar enlaces de los PR, commits individuales, revisión auténtica, ensayo de instalación
y hoja de demo humana. No declarar CHK013 cumplido por un PR o por ejecutar Playwright.
Cada integrante entrega además en Campus UCC según la instrucción docente comunicada;
el repositorio privado no sustituye esas cargas individuales.

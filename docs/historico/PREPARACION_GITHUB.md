# PreparaciÃ³n de GitHub â€” acciones propuestas, no ejecutadas

## Historial comprobado

| Commit | Autor registrado | AportaciÃ³n declarada por el usuario |
| --- | --- | --- |
| `58bab1f` | Danilo Carlosama / Danilo2334 | DocumentaciÃ³n SDD |
| `fd90a7d` | Danilo Carlosama / Danilo2334 | Backend y pruebas |
| `d680fb3` | Francisco Javier Molina Calderon / francisco3788 | Frontend y flujo completo |
| `d29b01b` | Francisco Javier Molina Calderon / francisco3788 | Correcciones, regresiones y cierre documental |

Los metadatos coinciden con la aclaraciÃ³n del usuario sobre el trabajo de cada integrante.
No prueban por sÃ­ solos quiÃ©n realizÃ³ el trabajo ni constituyen una revisiÃ³n independiente.
Ambos integrantes deben confirmar sus aportes desde sus cuentas reales. Las revisiones y PRs
siguen pendientes. No se modificaron autores, fechas ni historial durante esta preparaciÃ³n.

Correos de autor: Danilo `134672640+Danilo2334@users.noreply.github.com`;
Francisco `134155095+francisco3788@users.noreply.github.com`.
El committer de los cuatro commits es Danilo Carlosama; autor y committer son campos distintos.
La identidad Git configurada sigue siendo Danilo Carlosama con su correo noreply.
GitHub CLI reconoce Danilo2334 activo y francisco3788 autenticado inactivo; no se cambiaron cuentas.

`main` apunta a `58bab1f` y `feat/001-ecogest-mvp` a `d29b01b`.
La base comÃºn es `58bab1f87373d0110b088fc5d894a9f9f467e104`.
`git rev-list --left-right --count main...feat/001-ecogest-mvp` devuelve `0 3`.
Por tanto main tiene un commit vÃ¡lido y el PR incluirÃ¡ tres commits posteriores:
el commit SDD inicial estarÃ¡ en ambas ramas. No hace falta reescribir ni crear otra base.

El respaldo `backup/antes-correccion-autoria` apunta a `b855a1f` y es solo local.
No usar `git push --all`, `--mirror` ni force-push. No hay remoto configurado.
Las correcciones documentales actuales requieren revisiÃ³n y un nuevo commit autorizado
antes de publicarlas; no modificar los cuatro commits existentes.

## PublicaciÃ³n privada propuesta, solo despuÃ©s de autorizaciÃ³n

Destino propuesto: `Danilo2334/ecogest-360`; disponibilidad aÃºn no comprobada.
Antes de ejecutar, verificar cuenta activa, identidad, diff, secretos y estado limpio.
No imprimir tokens ni crear README/licencia remotos que introduzcan historia independiente.
Si ya existe origin o el repositorio, inspeccionarlo y ajustar el procedimiento sin sobrescribirlo.

```powershell
git status --short --branch
git diff --check
git config user.name
git config user.email
gh api user --jq .login
git remote -v
# Ejecutar lo siguiente Ãºnicamente con autorizaciÃ³n explÃ­cita:
gh repo create Danilo2334/ecogest-360 --private --source . --remote origin
git push -u origin main
git push -u origin feat/001-ecogest-mvp
gh repo edit Danilo2334/ecogest-360 --default-branch main
gh pr create --repo Danilo2334/ecogest-360 --base main --head feat/001-ecogest-mvp --draft --title "EcoGest 360: MVP ambiental y cierre de auditoria" --body-file docs/historico/PR_MVP_PROPUESTO.md
```

No se han ejecutado estas mutaciones. No usar `gh pr create --dry-run` como garantÃ­a de
no publicar: puede subir cambios. No se autoriza merge ni despliegue con este documento.

## ConfirmaciÃ³n y revisiÃ³n autÃ©ntica

1. Con autorizaciÃ³n, Danilo invita a `francisco3788`; Francisco acepta desde su cuenta.
2. Danilo confirma sus dos aportes y revisa frontend y cierre; Francisco confirma los
   dos aportes atribuidos y revisa backend/pruebas. Cada uno registra observaciones reales,
   archivos revisados y resultados en el PR desde su cuenta; no generar aprobaciones ficticias.
3. El PR abierto por Danilo puede recibir revisiÃ³n de Francisco. Danilo puede comentar
   su revisiÃ³n, pero no aprobar su propio PR. Registrar limitaciÃ³n de revisiÃ³n de cÃ³digo propio.
4. Para un PR independiente de Francisco, realizar un ensayo real de reproducciÃ³n del README
   y documentar resultados en `docs/VERIFICACION_INSTALACION_FRANCISCO.md`, con correcciones
   justificadas si existen. Crear rama `docs/francisco-reproduccion` desde la rama del MVP
   y PR hacia ella, o desde main y hacia main si el MVP ya se integrÃ³. Danilo revisa ese PR.
   No crear el informe ni un commit vacÃ­o para aparentar trabajo. Puede usarse otra copia
   de trabajo en este mismo PC; registrar que no es un segundo equipo independiente.
5. Guardar URLs de commits, PRs y revisiones, autores y fechas reales en la matriz docente.
   Aprobar o fusionar solo tras revisar y obtener autorizaciÃ³n; mantener el respaldo local.

## Evidencias acadÃ©micas pendientes

Consultar docs/entrega/CHECKLIST_ENTREGA.md. CHK013 requiere ejecuciÃ³n humana y registro real en
docs/entrega/REGISTRO_DEMO_HUMANA.md; un PR o Playwright no lo sustituye. Mantener cinco tareas TDD
histÃ³ricamente parciales. Cada integrante debe cargar su entrega en Campus UCC.
El PDF docente fue revisado externamente segÃºn la conversaciÃ³n y sigue fuera del repositorio.

## Comprobación local de publicación

Se revisaron 156 archivos candidatos y 162 blobs del historial de main/MVP: sin
coincidencias con secretos locales comprobados ni patrones de tokens/claves privadas buscados.
Es una revisión acotada, no una garantía absoluta de ausencia de secretos. `.gitignore`
excluye .env, entorno Python, node_modules, dist y adjuntos media; conserva artefactos SDD.
`git diff --check` sin errores. El árbol del respaldo y el del MVP son idénticos;
la corrección previa de autoría no cambió el contenido de aplicación.

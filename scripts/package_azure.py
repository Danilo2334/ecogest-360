"""Package explicit application sources; never include .env, media or local DBs."""
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APPS = ("config", "core", "organizations", "catalog", "waste", "traceability",
        "compost", "reports", "interventions", "intelligence")


def package():
    subprocess.run(["npm.cmd" if __import__("os").name == "nt" else "npm",
                    "--prefix", str(ROOT / "frontend"), "run", "build"], check=True)
    output = ROOT / "build" / "azure"
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "ecogest.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as target:
        backend = ROOT / "backend"
        for app in APPS:
            for source in sorted((backend / app).rglob("*.py")):
                if source.is_symlink():
                    raise ValueError("No se permiten enlaces simbólicos en el paquete")
                target.write(source, source.relative_to(backend).as_posix())
        target.write(backend / "manage.py", "manage.py")
        requirements = (backend / "requirements-azure.txt").read_text().replace(
            "-r requirements.txt", (backend / "requirements.txt").read_text())
        target.writestr("requirements.txt", requirements)
        for source in sorted((ROOT / "frontend" / "dist").rglob("*")):
            if source.is_file():
                if source.suffix not in {".html", ".js", ".css", ".svg", ".png", ".ico", ".woff2"}:
                    raise ValueError(f"Archivo inesperado en build: {source.name}")
                target.write(source, "web/" + source.relative_to(ROOT / "frontend" / "dist").as_posix())
    print(f"Paquete preparado: {archive} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    package()

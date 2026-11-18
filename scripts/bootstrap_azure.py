"""Initialize only the approved new Azure deployment; never reads local DB credentials."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
AZ = Path(os.environ["LOCALAPPDATA"]) / "Programs/AzureCLI-2.93.0/bin/az.cmd"
GROUP = "rg-ecogest360-demo"
PARAMS = json.loads((ROOT / "secrets/azure-deployment.parameters.json").read_text())["parameters"]
VALUES = {key: item["value"] for key, item in PARAMS.items()}


def az(*args):
    result = subprocess.run([str(AZ), *args, "--only-show-errors", "-o", "json"],
                            capture_output=True, text=True, check=False)
    if result.returncode:
        message = result.stderr
        for value in VALUES.values():
            if len(value) > 35:
                message = message.replace(value, "[REDACTED]")
        raise RuntimeError(message)
    return json.loads(result.stdout) if result.stdout.strip() else None


def main():
    import psycopg
    from psycopg import sql

    app = az("webapp", "show", "-g", GROUP, "-n", VALUES["appName"])
    host = app["defaultHostName"]
    server = az("postgres", "flexible-server", "show", "-g", GROUP, "-n", VALUES["postgresName"])
    dbhost = server["fullyQualifiedDomainName"]
    existing = az("postgres", "flexible-server", "firewall-rule", "list", "-g", GROUP,
                  "--server-name", VALUES["postgresName"])
    permitted = {rule["startIpAddress"] for rule in existing
                 if rule["startIpAddress"] == rule["endIpAddress"]}
    def allow_web(item):
        index, address = item
        if address in permitted:
            return
        az("postgres", "flexible-server", "firewall-rule", "create", "-g", GROUP,
           "--server-name", VALUES["postgresName"], "--name", f"ecogest-web-{index}",
           "--start-ip-address", address, "--end-ip-address", address)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(allow_web, enumerate(app["outboundIpAddresses"].split(","))))
    address = urllib.request.urlopen("https://api.ipify.org", timeout=20).read().decode().strip()
    import ipaddress
    ipaddress.IPv4Address(address)
    az("postgres", "flexible-server", "firewall-rule", "create", "-g", GROUP,
       "--server-name", VALUES["postgresName"], "--name", "ecogest-bootstrap-temporary",
       "--start-ip-address", address, "--end-ip-address", address)
    try:
        with psycopg.connect(host=dbhost, port=5432, dbname="ecogest", user="ecogest_admin",
                            password=VALUES["postgresAdminPassword"], sslmode="require",
                            connect_timeout=30, autocommit=True) as conn:
            exists = conn.execute("SELECT 1 FROM pg_roles WHERE rolname = 'ecogest_app'").fetchone()
            if not exists:
                conn.execute(sql.SQL("CREATE ROLE ecogest_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD {}").format(
                    sql.Literal(VALUES["appDatabasePassword"])))
            conn.execute("GRANT ecogest_app TO ecogest_admin")
            conn.execute("ALTER DATABASE ecogest OWNER TO ecogest_app")
            conn.execute("ALTER SCHEMA public OWNER TO ecogest_app")
            conn.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
            conn.execute("REVOKE ecogest_app FROM ecogest_admin")
        access_path = ROOT / "secrets/azure-access.json"
        if access_path.exists():
            access = json.loads(access_path.read_text())
        else:
            access = {"url": f"https://{host}", "password": secrets.token_urlsafe(24),
                      "users": [f"{prefix}_{role}" for prefix in ["demo", "intelligence"]
                                for role in ["administrador", "operador", "gestor", "consultor"]]}
            access_path.write_text(json.dumps(access, indent=2), encoding="utf-8")
        env = dict(os.environ, DB_HOST=dbhost, DB_PORT="5432", DB_NAME="ecogest",
                   DB_USER="ecogest_app", DB_PASSWORD=VALUES["appDatabasePassword"],
                   DJANGO_SECRET_KEY=VALUES["djangoSecretKey"], AZURE_APP_HOST=host,
                   DJANGO_SETTINGS_MODULE="config.settings_azure", DEMO_PASSWORD=access["password"],
                   AI_ENABLED="0", AI_BUDGET_AUTHORIZED="0", OPENAI_SMOKE_TEST="0")
        python = str(ROOT / "backend/.venv/Scripts/python.exe")
        for command in [("migrate", "--noinput"), ("seed_demo",),
                        ("seed_observatory_demo", "--apply", "--end-date", "2026-11-15")]:
            result = subprocess.run([python, "backend/manage.py", *command], cwd=ROOT, env=env,
                                    capture_output=True, text=True)
            if result.returncode:
                # Do not include full tracebacks or environment values in output.
                raise RuntimeError(f"El paso {command[0]} falló; revisar de forma privada.")
            print(f"Azure: {command[0]} completado.")
        with psycopg.connect(host=dbhost, port=5432, dbname="ecogest", user="ecogest_app",
                            password=VALUES["appDatabasePassword"], sslmode="require") as conn:
            flags = conn.execute("SELECT rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname=current_user").fetchone()
            assert flags == (False, False, False), "El rol tiene privilegios excesivos"
        if host != VALUES["appName"] + ".azurewebsites.net":
            az("webapp", "config", "appsettings", "set", "-g", GROUP, "-n", VALUES["appName"],
               "--settings", f"AZURE_APP_HOST={host}")
        print(f"Base y usuarios simulados preparados. URL: https://{host}")
        print("Credenciales nuevas guardadas solo en secrets/azure-access.json (ignorado por Git).")
    finally:
        # Removes only the temporary rule created by this script, not user resources.
        az("postgres", "flexible-server", "firewall-rule", "delete", "-g", GROUP,
           "--server-name", VALUES["postgresName"], "--name", "ecogest-bootstrap-temporary", "--yes")
        print("Acceso temporal de aprovisionamiento retirado.")


if __name__ == "__main__":
    main()

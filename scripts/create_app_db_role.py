"""One-time role setup for the newly created EcoGest local database only."""

import os
import secrets
from pathlib import Path
import psycopg
from psycopg import sql
from dotenv import load_dotenv, set_key

env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env)
if os.environ.get("DB_NAME") != "ecogest" or os.environ.get("DB_USER") != "ecogest":
    raise SystemExit(
        "No action: bootstrap identity does not match this new development database."
    )
password = secrets.token_urlsafe(32)
with psycopg.connect(
    dbname="ecogest",
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    autocommit=True,
) as conn:
    if conn.execute("SELECT 1 FROM pg_roles WHERE rolname='ecogest_app'").fetchone():
        raise SystemExit("No action: application role already exists.")
    conn.execute(
        sql.SQL(
            "CREATE ROLE ecogest_app LOGIN NOSUPERUSER NOCREATEROLE CREATEDB PASSWORD {}"
        ).format(sql.Literal(password))
    )
    conn.execute("ALTER DATABASE ecogest OWNER TO ecogest_app")
    conn.execute("GRANT USAGE, CREATE ON SCHEMA public TO ecogest_app")
    for (table,) in conn.execute(
        "SELECT tablename FROM pg_tables WHERE schemaname='public'"
    ).fetchall():
        conn.execute(
            sql.SQL("ALTER TABLE public.{} OWNER TO ecogest_app").format(
                sql.Identifier(table)
            )
        )
set_key(str(env), "POSTGRES_USER", os.environ["DB_USER"])
set_key(str(env), "POSTGRES_PASSWORD", os.environ["DB_PASSWORD"])
set_key(str(env), "DB_USER", "ecogest_app")
set_key(str(env), "DB_PASSWORD", password)
print(
    "Application role prepared: NOSUPERUSER, NOCREATEROLE; CREATEDB for isolated test databases. No secrets printed."
)

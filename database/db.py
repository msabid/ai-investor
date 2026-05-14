from sqlalchemy import create_engine, text
from pathlib import Path
from config.settings import SETTINGS

def get_engine():
    args = {"check_same_thread": False} if SETTINGS.database_url.startswith("sqlite") else {}
    return create_engine(SETTINGS.database_url, future=True, connect_args=args)

def init_db():
    if SETTINGS.database_url.startswith("sqlite"):
        Path("database").mkdir(exist_ok=True)
    schema = Path("database/schema.sql").read_text(encoding="utf-8")
    with get_engine().begin() as conn:
        for stmt in schema.split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.execute(text("INSERT OR IGNORE INTO risk_settings(id) VALUES (1)"))

def run_query(query, params=None):
    with get_engine().begin() as conn:
        return conn.execute(text(query), params or {})

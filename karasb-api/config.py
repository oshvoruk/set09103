from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "dev"
    DATABASE = BASE_DIR / "instance" / "karasb.db"
    SCHEMA_FILE = BASE_DIR / "schema.sql"

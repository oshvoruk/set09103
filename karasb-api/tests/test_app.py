from app import create_app
from config import Config


def test_create_app_loads_default_config(tmp_path, monkeypatch):
    database = tmp_path / "instance" / "test.db"
    monkeypatch.setattr(Config, "DATABASE", database)

    app = create_app()

    assert app.config["SECRET_KEY"] == "dev"
    assert app.config["DATABASE"] == database
    assert app.config["SCHEMA_FILE"] == Config.SCHEMA_FILE
    assert database.parent.is_dir()


def test_create_app_applies_test_config(tmp_path):
    database = tmp_path / "custom" / "test.db"

    app = create_app(
        {
            "SECRET_KEY": "test-secret",
            "DATABASE": database,
        }
    )

    assert app.config["SECRET_KEY"] == "test-secret"
    assert app.config["DATABASE"] == database
    assert database.parent.is_dir()

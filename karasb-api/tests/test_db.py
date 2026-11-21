import sqlite3

import pytest

from app import create_app
from app.db import get_db


@pytest.fixture
def app(tmp_path):
    return create_app(
        {
            "DATABASE": tmp_path / "test.db",
        }
    )


def test_init_db_command(app):
    result = app.test_cli_runner().invoke(args=["init-db"])

    assert result.exit_code == 0
    assert "initialised the database" in result.output

    with sqlite3.connect(app.config["DATABASE"]) as db:
        tables = db.execute(
            "select name from sqlite_master where type = 'table'"
        ).fetchall()

    assert {table[0] for table in tables} >= {
        "species",
        "watercourse",
        "site",
        "survey",
        "survey_species",
        "individual_fish_length",
    }


def test_get_db(app):
    with app.app_context():
        db = get_db()

        assert get_db() is db
        assert db.row_factory is sqlite3.Row

    # connection should be closed when application context ends
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute("select 1")

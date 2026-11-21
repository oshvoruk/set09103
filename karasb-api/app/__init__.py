from pathlib import Path

import click
from config import Config
from flask import Flask

from app.db import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("initialised the database")

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    return app

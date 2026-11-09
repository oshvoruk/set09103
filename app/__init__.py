from pathlib import Path

from flask import Flask

from app.db import close_db, init_db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)

    return app

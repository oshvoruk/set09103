import sqlite3

import click
from flask import current_app, g


@click.command("init-db")
def init_db():
    with open(current_app.config["SCHEMA_FILE"], encoding="utf-8") as f:
        get_db().executescript(f.read())

    click.echo("Initialised the database")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

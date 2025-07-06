import click
from flask.cli import with_appcontext
from flask_migrate import migrate, upgrade


def register_commands(app):
    @app.cli.command("db_auto_migrate")
    @with_appcontext
    def auto_migrate():
        migrate(message="Auto migration")
        upgrade()
        print("[Auto migration & upgrade done]")

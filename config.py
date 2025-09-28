# App/cli.py
import click
from flask.cli import with_appcontext
from App.database import db

@click.command("init")
@with_appcontext
def init_db():
    """Initialize the database (create tables)."""
    db.create_all()
    click.echo("Database initialized!")

def register(app):
    app.cli.add_command(init_db)


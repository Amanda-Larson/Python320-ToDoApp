"""convert menu based program to a cli program using typer , rich, and sqlite3"""

import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command(short_help="Adds a task and related information to the task database.")
def add(task_nm, task_desc, due_date):
    typer.echo(f'Adding {task_nm} to the list.')


if __name__=='__main__':
    app()
"""new file to experiment with creating a CLI app with typer, rich, and sqlite3
created with the help of the youtube video: https://youtu.be/ynd67UwG_cI"""

import typer
from rich.console import Console
# from rich.table import Table
from tasks import Tasks as t

console = Console()

app = typer.Typer()


@app.command(short_help="Add a task to the to-do list")
def add(task_nm: str, task_desc: str, due_date: str):
    t.add_task(task_nm, task_desc, due_date)
    typer.secho(f"Adding, '{task_nm}'to the list.", fg=typer.colors.BRIGHT_CYAN)


# @app.command(short_help="Updates a task in the task database")
# def update(task_nm: str, task_desc: str, due_date: str):
#     t.update_task(task_nm, task_desc, due_date)
#     typer.secho(f"Updating {task_nm}...")


@app.command(help="Delete a task")
def delete(task_name: str = typer.Option(default=None, prompt="Task name to delete",
                                         help="Name of the task to be deleted")):
    t.delete_task(task_name)
    typer.echo(f'{task_name} has been deleted.')


@app.command(short_help="Print a table of tasks and related information")
def print_all_tasks():
    table = []
    query = t.select().tuples()
    for row in query:
        table.append(row)
    t.generate_report(table)


@app.command(short_help="List tasks by Task ID")
def list_by_num(choice: str = typer.Option(default=None,
                                           prompt="Enter 1 for Ascending or 2 for Descending",
                                           prompt_required=True)):
    t.task_by_number(choice)


@app.command(short_help="List tasks by priority")
def list_by_priority(choice: str = typer.Option(default=None,
                                                prompt="Enter 1 for Ascending or 2 for Descending",
                                                prompt_required=True)):
    t.task_by_priority(choice)


@app.command(short_help="List tasks by due date")
def list_by_due_date(choice: str = typer.Option(default=None,
                                                prompt="Enter 1 for Ascending or 2 for Descending",
                                                prompt_required=True)):
    t.task_by_due_date(choice)


@app.command(short_help="List completed tasks")
def list_completed(choice: str = typer.Option(default=None,
                                              prompt="Enter 1 for Ascending or 2 for Descending",
                                              prompt_required=True)):
    t.list_completed(choice)


if __name__ == "__main__":
    t.db_connect()
    app()
    print('got to here')

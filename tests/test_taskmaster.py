from typer.testing import CliRunner
import pysnooper
from src.ToDoListApp.taskmaster import app
import src.ToDoListApp.taskmaster as tm
from src.ToDoListApp.tasks import Tasks, DeletedTasks
import peewee as pw
import pysnooper
from peewee import SqliteDatabase

runner = CliRunner()

database = SqliteDatabase(':memory:')
MODELS = [Tasks, DeletedTasks]


def use_test_db(fn):
    @pw.wraps(fn)
    def inner(self):
        with database.bind_ctx(MODELS):
            database.create_tables(MODELS)
            try:
                fn(self)
            finally:
                database.drop_tables(MODELS)


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 2


def test_add():
    with database.bind_ctx(MODELS):
        database.create_tables(MODELS)
        try:
            result = runner.invoke(app, tm.add('example task', 'example description', '07/07/2022'))
            assert 'Adding example task to the list.', '\n' in result.stdout
        finally:
            database.drop_tables(MODELS)


def test_delete():
    result = runner.invoke(app)
    tm.delete('example task')
    assert 'example task has been deleted.' in result.stdout

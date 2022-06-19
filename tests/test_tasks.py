import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from peewee import SqliteDatabase
import peewee as pw
import pysnooper
from src.ToDoListApp.tasks import Tasks, DeletedTasks
import src.ToDoListApp.tasks as t


# database = SqliteDatabase(':memory:')
# MODELS = [Tasks, DeletedTasks]
#
# def use_test_db(fn):
#     @pw.wraps(fn)
#     def inner(self):
#         with database.bind_ctx(MODELS):
#             database.create_tables(MODELS)
#             try:
#                 fn(self)
#             finally:
#                 database.drop_tables(MODELS)


class TestTasks(TestCase):
    def setUp(self):
        database = SqliteDatabase(':memory:')
        database.connect()

        # Creation of the database
        database.create_tables([
            Tasks,
            DeletedTasks
        ])

        # Create default task
        task_nm = 'setup task'
        task_desc = 'setup task description'
        due_date = '06/25/2022'
        self.assertTrue(Tasks.add_task(task_nm, task_desc, due_date))

    def test_add_task(self):
        task_nm = 'anything task'
        task_desc = 'sample task description'
        due_date = '06/29/2022'
        self.assertTrue(Tasks.add_task(task_nm, task_desc, due_date))

    def test_add_task_duplicated(self):
        task_nm = 'setup task'
        task_desc = 'setup task description'
        due_date = '06/25/2022'
        dup = Tasks.add_task(task_nm, task_desc, due_date)
        self.assertFalse(dup)
        # self.assertRaises(pw.IntegrityError)

    def test_delete_user(self):
        task_name = 'setup task'
        self.assertEqual(Tasks.delete_task(task_name), True)


    def tearDown(self):
        database = SqliteDatabase(':memory:')
        database.drop_tables([
            Tasks,
            DeletedTasks
        ])
        database.close()

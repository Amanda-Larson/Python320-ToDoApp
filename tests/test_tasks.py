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
        self.assertEqual(Tasks.add_task(task_nm, task_desc, due_date), True)

    def test_add_task(self):
        task_nm = 'sample tasks'
        task_desc = 'sample task description'
        due_date = '06/29/2022'
        self.assertEqual(Tasks.add_task(task_nm, task_desc, due_date), True)
        # self.assertRaises(pw.IntegrityError)

    def test_add_task_duplicated(self):
        task_nm = 'sample tasks'
        task_desc = 'sample task description'
        due_date = '06/29/2022'
        self.assertEqual(Tasks.add_task(task_nm, task_desc, due_date), False)

    def test_modify_task(self):
        user_id = 'ldconejo79'
        user_name = 'Elisa'
        user_last_name = 'Cornejo'
        user_email = 'elisa.conejo@conejo.com'
        self.assertEqual(self.user_collection.modify_user(user_id, user_email, user_name, user_last_name), True)

    def test_modify_user_not_found(self):
        user_id = 'ldconejo80'
        user_name = 'Elisa'
        user_last_name = 'Cornejo'
        user_email = 'elisa.conejo@conejo.com'
        self.assertEqual(self.user_collection.modify_user(user_id, user_email, user_name, user_last_name), False)

    def test_search_user(self):
        user_id = 'ldconejo79'
        user_name = 'Luis'
        user_last_name = 'Conejo'
        user_email = 'luisconejo@conejo.com'
        result = self.user_collection.search_user(user_id)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.user_name, user_name)
        self.assertEqual(result.user_last_name, user_last_name)
        self.assertEqual(result.user_email, user_email)

    def test_search_user_not_found(self):
        user_id = 'ldconejo80'
        result = self.user_collection.search_user(user_id)
        self.assertEqual(result, None)

    def test_delete_user(self):
        user_id = 'ldconejo79'
        self.assertEqual(self.user_collection.delete_user(user_id), True)

    def tearDown(self):
        database = SqliteDatabase(':memory:')
        database.drop_tables([
            Tasks,
            DeletedTasks
        ])
        database.close()

import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from peewee import SqliteDatabase
import pysnooper
import tasks


class TestSocialNetwork(TestCase):
    def setUp(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.database.pragma('foreign_keys', 1, permanent=True)
        # Creation of the database
        self.database.create_tables([
            UsersTable,
            StatusTable
        ])
        self.user_collection = users.UserCollection(self.database)
        self.status_collection = user_status.UserStatusCollection(self.database)

        # Create default user
        user_id = 'ldconejo79'
        user_name = 'Luis'
        user_last_name = 'Conejo'
        user_email = 'luisconejo@conejo.com'
        self.assertEqual(self.user_collection.add_user(user_id, user_email, user_name, user_last_name), True)

        # Create default status
        status_id = 'ldconejo79_001'
        status_text = 'My first status'
        self.assertEqual(self.status_collection.add_status(user_id, status_id, status_text), True)

    def test_add_user(self):
        user_id = 'ldconejo80'
        user_name = 'Luis'
        user_last_name = 'Conejo'
        user_email = 'luisconejo@conejo.com'
        self.assertEqual(self.user_collection.add_user(user_id, user_email, user_name, user_last_name), True)

    def test_add_user_duplicated(self):
        user_id = 'ldconejo79'
        user_name = 'Luis'
        user_last_name = 'Conejo'
        user_email = 'luisconejo@conejo.com'
        self.assertEqual(self.user_collection.add_user(user_id, user_email, user_name, user_last_name), False)

    def test_modify_user(self):
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

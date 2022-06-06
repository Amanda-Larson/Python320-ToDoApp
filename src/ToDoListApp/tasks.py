"""
# Header
# File: tasks.py
# Author: Amanda
# Started: 6-4-2022
# Updated:
"""  # -------------------------------#"""

import os
import datetime
import peewee as pw
from loguru import logger

# check to see if the files exists, if it does, delete it
file = 'to_do_list.db'
# if os.path.exists(file):
#     os.remove(file)

# connect to the database
db = pw.SqliteDatabase(file)


# set up a base model for inheritance into the classes which become database tables
class BaseModel(pw.Model):
    logger.info("allows database to be defined or changed in one place")

    class Meta:
        database = db


class Tasks(BaseModel):
    """Contains a collection of tasks"""

    task_id = pw.CharField(primary_key=True, max_length=14)
    task_nm = pw.CharField(max_length=30, unique=True,
                           constraints=[pw.Check("LENGTH(task_nm) < 30")])
    task_desc = pw.CharField(max_length=100,
                             constraints=[pw.Check("LENGTH(task_desc) < 100")])
    start_date = pw.DateField(formats='%m-%d-%Y')

    due_date = pw.DateField(formats='%m-%d-%Y')

    priority = pw.CharField()

    status = pw.CharField(max_length=20, default='In Progress...')

    @staticmethod
    def db_connect():
        """This connects the database and sets up a table"""
        logger.info("Set up the database.")
        db.connect()
        # db.execute_sql('PRAGMA foreign_keys = ON;')
        db.create_tables([Tasks])
        db.create_tables([DeletedTasks])
        logger.info('db is connected, Tasks table and Deleted Tasks table are created')

    @staticmethod
    def add_task(task_nm, task_desc, start_date, due_date, priority):
        # create task id
        task_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            new_task = Tasks.create(task_id=task_id, task_nm=task_nm, task_desc=task_desc, start_date=start_date,
                                    due_date=due_date, priority=priority)

            new_task.save()
            return True
        except pw.IntegrityError as error:
            logger.info(error)
            logger.exception(error)
            return False

    @staticmethod
    def calc_priority():

        get_due_date = datetime.datetime.strptime((input('Task due date (Please enter in MM/DD/YYYY format): ')),
                                                  '%m/%d/%Y')
        due_date = datetime.datetime.strftime(get_due_date, '%m-%d-%Y')
        today = datetime.datetime.now()
        one_week = datetime.timedelta(days=7)  # less than 7 days is urgent
        two_weeks = datetime.timedelta(days=14)  # less than 7 days is urgent

        high = today + one_week
        med = today + two_weeks

        try:
            if today < get_due_date < high:
                # print('urgent')
                # priority = 'high'
                return due_date, 'high'
            elif high < get_due_date < med:
                return due_date, 'medium'
            elif get_due_date > med:
                return get_due_date, 'low'
            else:
                print('Please try again using the correct date format (MM/DD/YYYY)')
        except ValueError:
            print("Error: must be in MM/DD/YYYY format, please try again.")

    def update_task():
        pass

    def list_tasks():
        pass

    def mark_complete(del_task):
        pass

    @staticmethod
    def delete_task(task_name):
        """Deletes an existing task"""
        del_task = Tasks.get(Tasks.task_nm == task_name)
        logger.info(f'The task to be deleted is {del_task}')
        DeletedTasks.create(task_id=del_task.task_id,
                            task_nm=del_task.task_nm,
                            task_desc=del_task.task_desc,
                            start_date=del_task.start_date,
                            due_date=del_task.due_date,
                            priority=del_task.priority,
                            status=del_task.status)
        del_task.delete_instance()

    @staticmethod
    def generate_report(table):
        header = ['Task Name', 'Task Description', 'Task Start Date', 'Task Due Date', 'Priority', 'Task Status']
        print(f'{"================== Task Master To-Do List ==================":^115}')
        print()
        print(f'{header[0]:<15}{header[1]:<30}{header[2]:<20}{header[3]:<20}{header[4]:<20}{header[5]:<20}')
        for row in table:
            print(f'{row[1]:<15}{row[2]:<30}{row[3]:<20}{row[4]:<20}{row[5]:<20}{row[6]:<20}')
        print(f'{"=" * 75:^115}')


class DeletedTasks(BaseModel):
    """Contains a collection of tasks"""

    task_id = pw.CharField(primary_key=True, max_length=14)
    task_nm = pw.CharField(max_length=30, unique=True,
                           constraints=[pw.Check("LENGTH(task_nm) < 30")])
    task_desc = pw.CharField(max_length=100,
                             constraints=[pw.Check("LENGTH(task_desc) < 100")])
    start_date = pw.DateField(formats='%m-%d-%Y')

    due_date = pw.DateField(formats='%m-%d-%Y')

    priority = pw.CharField()

    status = pw.CharField(max_length=20, default='In Progress...')

    # @staticmethod
    # def db_connect():
    #     """This connects the database and sets up a table"""
    #     logger.info("Set up the database.")
    #     db.connect()
    #     # db.execute_sql('PRAGMA foreign_keys = ON;')
    #     db.create_tables([DeletedTasks])
    #     logger.info('db is connected, Tasks table is created')


class Format:
    end = '\033[0m'
    underline = '\033[4m'

# print(Format.underline + 'Your text here' + Format.end)
# how to print an empty check box '\u25FB' +

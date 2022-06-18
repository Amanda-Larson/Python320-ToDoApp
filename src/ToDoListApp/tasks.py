"""
# Header
# File: tasks.py
# Author: Amanda
# Started: 6-4-2022
# Updated:
"""  # -------------------------------#"""

# import os
import datetime
import pysnooper
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

    complete_date = pw.DateField(formats='%m-%d-%Y')

    @staticmethod
    def db_connect():
        """This connects the database and sets up a table"""
        db.connect()
        # db.execute_sql('PRAGMA foreign_keys = ON;')
        db.create_tables([Tasks])
        db.create_tables([DeletedTasks])

    @staticmethod
    def add_task(task_nm, task_desc, due_date):
        # create task id
        task_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # create start date as today
        start_date = datetime.datetime.now().strftime('%m-%d-%Y')
        # normalize due_date
        date_obj = Tasks.normalize_date(due_date)
        # calc priority
        priority = Tasks.calc_priority(due_date)
        complete_date = ''
        try:
            new_task = Tasks.create(task_id=task_id, task_nm=task_nm, task_desc=task_desc, start_date=start_date,
                                    due_date=date_obj, priority=priority, complete_date=complete_date)

            new_task.save()
            return True
        except pw.IntegrityError as error:
            # logger.exception(error)
            return False

    @staticmethod
    def calc_priority(due_date):
        try:
            while True:
                due_date = datetime.datetime.strptime(due_date, '%m/%d/%Y')
                if due_date > datetime.datetime.now():
                    # here, we do some date math to figure out task priority...
                    today = datetime.datetime.now()
                    one_week = datetime.timedelta(days=7)  # less than 7 days is urgent
                    two_weeks = datetime.timedelta(days=14)  # less than 7 days is urgent

                    high = today + one_week
                    med = today + two_weeks

                    if today < due_date < high:
                        return 'High'
                    if high < due_date < med:
                        return 'Medium'
                    if due_date > med:
                        return 'Low'

                else:
                    print('ERROR: Date must be in the future.)')
        except ValueError:
            print("Error: must be in MM/DD/YYYY format, please try again.")

    @staticmethod
    # @pysnooper.snoop()
    def normalize_date(due_date):
        new_date = '-'.join(str.zfill(elem, 2) for elem in due_date.split('/'))
        # date_obj = datetime.datetime.strptime(new_date, '%m-%d-%Y')
        return new_date


    @staticmethod
    def update_task():
        pass

    @staticmethod
    def task_by_number(order: str):
        """sort tasks based on submenu selection"""
        try:
            if order == '1':
                print(Format.underline + '\nTasks Sorted By Task ID:' + Format.end)
                for row in Tasks.select().order_by(+Tasks.task_id):
                    print(row.task_id + " " + row.task_nm)
            elif order == '2':
                print(Format.underline + '\nTasks Sorted By Task ID:' + Format.end)
                for row in Tasks.select().order_by(-Tasks.task_id):
                    print(row.task_id + " " + row.task_nm)
        except ValueError as error:
            print(error)
            logger.info(error)

    @staticmethod
    def task_by_priority(order):
        try:
            if order == '1':
                print(Format.underline + '\nTasks sorted by Priority (Low to High):' + Format.end)
                for row in Tasks.select().where(Tasks.priority == 'Low'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
                for row in Tasks.select().where(Tasks.priority == 'Medium'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
                for row in Tasks.select().where(Tasks.priority == 'High'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
            elif order == '2':
                print(Format.underline + '\nTasks sorted by Priority (High to Low):' + Format.end)
                for row in Tasks.select().where(Tasks.priority == 'High'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
                for row in Tasks.select().where(Tasks.priority == 'Medium'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
                for row in Tasks.select().where(Tasks.priority == 'Low'):
                    print(Format.checkbox + row.task_nm + ": " + row.priority)
        except ValueError as error:
            print(error)
            logger.info()

    @staticmethod
    def task_by_due_date(order):
        try:
            if order == '1':
                print(Format.underline + '\nTasks sorted by Due Date (Ascending):' + Format.end)
                for row in Tasks.select().order_by(+Tasks.due_date):
                    print(row.task_nm + ": " + 'Due: ' + row.due_date)
            elif order == '2':
                print(Format.underline + '\nTasks sorted by Due Date (Descending):' + Format.end)
                for row in Tasks.select().order_by(-Tasks.due_date):
                    print(row.task_nm + ": " + 'Due: ' + row.due_date)
        except ValueError as error:
            print(error)
            logger.info()

    @staticmethod
    def list_completed(order):
        try:
            if order == '1':
                date_one = datetime.datetime.strptime((input('What is your start date (MM/DD/YYYY): ')), '%m/%d/%Y')
                date_two = datetime.datetime.strptime((input('What is your end date (MM/DD/YYYY): ')), '%m/%d/%Y')
                print(Format.underline + '\nCompleted Tasks in Date Range (Ascending):' + Format.end)
                date_range = Tasks.select().where(
                    (Tasks.due_date.between(date_one, date_two)) and (Tasks.status == 'Complete'))
                for row in date_range.order_by(+Tasks.due_date):
                    print(Format.checkmark + " " + row.task_nm + ": " + 'Due: ' + row.due_date)
            elif order == '2':
                date_one = datetime.datetime.strptime((input('What is your start date (MM/DD?YYYY): ')), '%m/%d/%Y')
                date_two = datetime.datetime.strptime((input('What is your end date (MM/DD?YYYY): ')), '%m/%d/%Y')
                print(Format.underline + '\nCompleted Tasks in Date Range (Descending):' + Format.end)
                date_range = Tasks.select().where(
                    (Tasks.due_date.between(date_one, date_two)) and (Tasks.status == 'Complete'))
                for row in date_range.order_by(-Tasks.due_date):
                    print(Format.checkmark + " " + row.task_nm + ": " + 'Due: ' + row.due_date)
        except ValueError as error:
            print(error)
            logger.info()

    @staticmethod
    def mark_complete(task_name):
        """mark a task complete"""
        try:
            query = Tasks.get(Tasks.task_nm == task_name)
            query.status = 'Complete'
            query.save()
            logger.info(f'Task name: {task_name} is now complete')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not find {task_name}, please try again.')
            return False

    @staticmethod
    def delete_task(task_name):
        """Deletes an existing task"""
        del_task = Tasks.get(Tasks.task_nm == task_name)
        DeletedTasks.create(task_id=del_task.task_id,
                            task_nm=del_task.task_nm,
                            task_desc=del_task.task_desc,
                            start_date=del_task.start_date,
                            due_date=del_task.due_date,
                            priority=del_task.priority,
                            status=del_task.status,
                            complete_date=del_task.complete_date)
        del_task.delete_instance()

    @staticmethod
    def generate_report(table):
        header = ['Task Name'.upper(), 'Task Description'.upper(), 'Task Start Date'.upper(), 'Task Due Date'.upper(),
                  'Priority'.upper(), 'Task Status'.upper()]
        print(f'{"================== Task Master To-Do List ==================":^115}')
        print()
        print(f'{header[0]:<20}{header[1]:<30}{header[2]:<20}{header[3]:<20}{header[4]:<20}{header[5]:<20}')
        for row in table:
            print(f'{row[1]:<20}{row[2]:<30}{row[3]:<20}{row[4]:<20}{row[5]:<20}{row[6]:<20}')
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


class Format:
    """this is for fancy stuff"""
    end = '\033[0m'
    underline = '\033[4m'
    checkbox = ('\u25FB' + ' ')
    checkmark = '\u2714'

# print(Format.underline + 'Your text here' + Format.end)
# how to print an empty check box '\u25FB' +


# if __name__ == "__main__":
#     # Tasks.db_connect()
#     app()
#     print('got to here')

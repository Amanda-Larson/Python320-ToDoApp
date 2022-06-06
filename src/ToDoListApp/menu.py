import sys
from loguru import logger
import pysnooper
import datetime
import tasks

logger.info("Let's get to debugging")
logger.add("out.log", backtrace=True, diagnose=True)


def load_tasks():
    pass


def add_task():
    """add new tsk"""
    task_nm = input('Task name: ')
    task_desc = input('Task description: ')
    start_date = datetime.datetime.now().strftime('%m-%d-%Y')
    due_date, priority = tasks.Tasks.calc_priority()
    if not tasks.Tasks.add_task(task_nm, task_desc, start_date, due_date, priority):
        print('task not added')
    else:
        print('task added')


def update_task():
    pass


def list_tasks():
    """list all tasks"""
    query = tasks.Tasks.select().tuples()
    for row in query:
        print(row)


def mark_complete():
    pass


def delete_task():
    generate_report()
    task_name = input('Please type the task name of the task you\'d like to delete: ')
    if not tasks.Tasks.delete_task(task_name):
        print('Task was successfully deleted.')
    else:
        print('An error occurred while trying to delete task')


def generate_report():
    table = []
    query = tasks.Tasks.select().tuples()
    for row in query:
        table.append(row)
    return tasks.Tasks.generate_report(table)


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == '__main__':
    # task database connection
    tasks.Tasks.db_connect()
    # tasks.DeletedTasks.db_connect()
    # load tasks on startup

    menu_options = {
        'A': add_task,
        'B': update_task,
        'C': list_tasks,
        'D': mark_complete,
        'E': delete_task,
        'F': generate_report,
        'Q': quit_program
    }

    while True:
        user_selection = input("""
        
                Welcome to Task Master
        Please make a choice from the menu below:
        
        A: Add a task
        B: Update a task (change task name, description, or dates)
        C: List all tasks
        D: Mark a task complete
        E: Delete a task from the list
        F: Generate a to-do list report (full report)
        Q: Quit
        
        Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")

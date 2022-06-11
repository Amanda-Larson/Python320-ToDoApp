import sys
from loguru import logger
import pysnooper
import datetime
import tasks
import peewee as pw

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


#
# def list_tasks():
#     """list all tasks"""
#     query = tasks.Tasks.select().tuples()
#     for row in query:
#         print(row)

# @pysnooper.snoop(depth=2)
def list_tasks():
    """sort tasks by"""
    while True:
        try:
            submenu_selection = input("""
Would you like to:
    a: List All Tasks by Task Number
    b: List Open Tasks by Priority
    c: List Open Tasks by Due Date
    d: List Completed Tasks in Date Range
    e: List All Overdue Tasks
    f: Return to Main Menu
    
Please enter your choice: """)
            if submenu_selection == 'F'.lower():
                print('Okay, back to main menu.')
                break
            else:
                sort_dir = int(input("""
Would you like to sort the tasks ascending or descending?
1: Ascending
2: Descending
"""))
                if not tasks.Tasks.list_tasks(submenu_selection, sort_dir):
                    print('--End of List--')
                # return submenu_selection, sort_dir
        except ValueError as error:
            print(f'Please choose a number. {error}')
            return False


def mark_complete():
    """mark a task complete"""
    completed = input('Which task would you like to mark completed? ')
    try:
        if tasks.Tasks.mark_complete(completed):
            print('Task was successfully marked complete.')
        else:
            print('An error occurred while trying to complete task, please try again.')
    except pw.DoesNotExist:
        print('Uh oh - that task does not exist, please try again.')


def delete_task():
    """Deletes a task by removing it from the tasks table and moving it to the deleted tasks table."""
    generate_report()
    task_name = input('Please type the task name of the task you\'d like to delete: ')
    try:
        if not tasks.Tasks.delete_task(task_name):
            print('Task was successfully deleted.')
        else:
            print('An error occurred while trying to delete task')
    except pw.DoesNotExist:
        print('Uh oh - that task does not exist, please try again.')


def generate_report():
    """Generates a report table of all the tasks and related data"""
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

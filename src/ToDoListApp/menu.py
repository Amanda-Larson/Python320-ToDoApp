import sys
from loguru import logger
import pysnooper
import main

logger.info("Let's get to debugging")
logger.add("out.log", backtrace=True, diagnose=True)



def load_tasks():
    pass


def add_task():
    pass


def update_task():
    pass


def list_tasks():
    pass


def mark_complete():
    pass


def delete_task():
    pass


def generate_report():
    pass


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == '__main__':
    # task database connection

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
        'A': Add a task
        'B': Update a task (change task name, description, or dates)
        'C': List all tasks
        'D': Mark a task complete
        'E': Delete a task from the list
        'F': Generate a to-do list report (full report)
        'Q': Quit
        
        Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")

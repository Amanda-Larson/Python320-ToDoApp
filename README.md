#Introduction
You are to build a python todo application for your personal use. It will keep track of your tasks and report upon them. You can use whatever programming model you deem most appropriate (OO or functions).

##Part 1
The app will be driven by the command line. Thus, you will use simple terminal IO (input and print) as a user interface for now. It will support the following commands:

1. add new task
2. list tasks
3. set a start date for the task
4. set a due date for the task
5. mark the task as completed
6. delete a task
7. generate report
8. change task name
9. change task description

All tasks will be stored in a database. You can use sqlite, mongodb, or any other database of your choice.

The following data is kept for each task:

1. Task number (not editable after adding)
2. Task name
3. Task descrption
4. Task start date
5. Task due date
6. Task priority

Task name and task description are mandatory when adding a new task. All other fields are optional, and can be added via the command line.

The task app must produce the following lists:

1. List all tasks sorted by task number
2. List all tasks sorted by priority
3. List all open tasks sorted by due date
4. List all closed tasks between specified dates
5. List all overdue tasks

All lists must be correctly formatted for display in a terminal.

You should develop extensive automated tests as part of building this system.

##Part 2 (after week 9 lesson):
Build an API to the task app, using curl to enter commands, and returning the results as json structures.

Your application must be built so that you can either use the terminal or curl interface.

More news on part 2 in weeks 8 & 9

 

Here is what you need to do:

Use pyscaffold to develop a robust project structure. Use a virtual environment and git.

Use automated testing to validate the system behaves as intended.
Develop the data capture functionality.
Make sure the data is validated, so data entry errors can be prevented as much as possible.
Ensure each task has a unique id.
Make use of formatting techniques to ensure that information reported to the screen is well laid out and easy to understand.
Be sure task is stored in the database. "Deleted" tasks are not to be removed; rather, they are marked as deleted.
Be sure to commit to local git frequently and use a virtual environment.


##Submission:
Your submission should include the following:

The py files, including tests, that you develop.
Tests that use test data to show the system works (you can mock the database if you chose).
Run git log > history.txt in the terminal from your project root directory to show how you have committed regularly.
The files should be zipped and attached to your Canvas submission.


##Tips
Be creative! Use this as an opportunity to reflect on everything you have learned so far and apply it to application development.
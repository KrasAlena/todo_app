import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.date_completed = None

    def complete(self):
        self.completed = True
        self.date_completed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.completed_tasks_file = 'completed_tasks.json'

    def add_task(self, description):
        if description.strip():  # Check if description is not empty after stripping whitespace
            task = Task(description)
            self.tasks.append(task)

    def complete_task(self, index):
        self.tasks[index].complete()

    def clear_completed_tasks(self):
        completed_tasks = [task for task in self.tasks if task.completed]
        if completed_tasks:
            with open(self.completed_tasks_file, 'a') as file:
                for task in completed_tasks:
                    task_data = {
                        'description': task.description,
                        'date_added': task.date_added,
                        'date_completed': task.date_completed
                    }
                    file.write(json.dumps(task_data) + '\n')
            self.tasks = [task for task in self.tasks if not task.completed]

task_manager = TaskManager()

@app.route('/')
def index():
    return render_template('index.html', tasks=task_manager.tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    description = request.form['task']
    task_manager.add_task(description)
    return redirect(url_for('index'))

@app.route('/complete_task/<int:index>')
def complete_task(index):
    task_manager.complete_task(index)
    return redirect(url_for('index'))

@app.route('/clear_completed_tasks', methods=['GET', 'POST'])
def clear_completed_tasks():
    if request.method == 'POST':
        task_manager.clear_completed_tasks()
        return redirect(url_for('index'))
    else:
        # Handle GET request (if needed)
        pass



if __name__ == '__main__':
    app.run(debug=True)

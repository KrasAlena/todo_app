import json
from datetime import datetime


class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.date_completed = None

    def complete(self):
        self.completed = True
        self.date_completed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        status = 'Completed' if self.completed else 'Pending'
        return f'{self.description} - {status}'


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.saved_completed_tasks = set()

    def add_task(self, description):
        if description.strip():
            task = Task(description)
            self.tasks.append(task)
        else:
            print('Task description cannot be empty.')

    def complete_task(self, index):
        if TaskManager._is_valid_index(self.tasks, index):
            self.tasks[index].complete()
        else:
            print('Invalid task index.')

    def delete_task(self, index):
        if TaskManager._is_valid_index(self.tasks, index):
            del self.tasks[index]
        else:
            print('Invalid task index.')

    def display_tasks(self):
        if self.tasks:
            for i, task in enumerate(self.tasks):
                print(f'{i + 1}. {task}')
        else:
            print('No tasks.')

    def save_completed_tasks(self, filename='completed_console.json'):
        """
            Save completed tasks to a JSON file, avoiding duplicates.

            This method iterates over the list of tasks, calculates the completion time for each completed task,
            and constructs a dictionary representing the completed task data. It then checks if the task data
            is already present in the set of saved completed tasks to avoid duplicates. If not, it appends
            the task data to the list of completed tasks and adds the task data to the set of saved completed tasks.
            Finally, it writes each completed task data as a JSON object to the specified file, with each object
            written on a new line.

            Parameters:
                filename (str): The name of the JSON file to save the completed tasks. Default is 'completed_console.json'.

            Returns:
                None

            Side Effects:
                - Writes completed task data to a JSON file.
                - Modifies the set of saved completed tasks.

            Example Usage:
                task_manager.save_completed_tasks()
            """
        completed_tasks = []
        for task in self.tasks:
            if task.completed and task.date_completed and task.date_added:
                completion_time = round(((datetime.strptime(task.date_completed, '%Y-%m-%d %H:%M:%S') - datetime.strptime(task.date_added, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600), 4)
                completed_task_data = {'description': task.description, 'completed': task.completed, 'completion_time': completion_time}
                if tuple(completed_task_data.items()) not in self.saved_completed_tasks:
                    completed_tasks.append(completed_task_data)
                    self.saved_completed_tasks.add(tuple(completed_task_data.items()))

        with open(filename, 'a') as file:
            for task_data in completed_tasks:
                json.dump(task_data, file)
                file.write('\n')

    @classmethod
    def _is_valid_index(cls, tasks, index):
        return 0 <= index < len(tasks)

    @classmethod
    def from_file(cls, filename):
        manager = cls()
        with open(filename, 'r') as file:
            data = json.load(file)
            for task_data in data:
                task = Task(task_data['description'])
                task.completed = task_data['completed']
                manager.tasks.append(task)
        return manager


def main():
    task_manager = TaskManager()

    while True:
        print('\nTodo List action:')
        print('1. Add Task')
        print('2. Complete Task')
        print('3. Delete Task')
        print('4. Display Tasks')
        print('5. Load Tasks from File')
        print('6. Save Completed Tasks')
        print('7. Exit')

        choice = input('Enter your choice: ')

        if choice == '1':
            description = input('Enter task description: ')
            task_manager.add_task(description)
        elif choice == '2':
            index = int(input('Enter task index to mark as complete: ')) - 1
            task_manager.complete_task(index)
        elif choice == '3':
            index = int(input('Enter task index to delete: ')) - 1
            task_manager.delete_task(index)
        elif choice == '4':
            task_manager.display_tasks()
        elif choice == '5':
            filename = input('Enter filename to load tasks from: ')
            task_manager = TaskManager.from_file(filename)
        elif choice == '6':
            task_manager.save_completed_tasks()
            print('Completed tasks saved to "completed.json".')
        elif choice == '7':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()


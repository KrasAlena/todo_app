class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
        else:
            print('Invalid task index.')

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print('Invalid task index.')

    def display_tasks(self):
        if self.tasks:
            for i, task in enumerate(self.tasks):
                status = 'Completed' if task.completed else 'Pending'
                print(f'{i + 1}. {task.description} - {status}')
        else:
            print('No tasks.')


def main():
    task_manager = TaskManager()

    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Complete Task")
        print("3. Delete Task")
        print("4. Display Tasks")
        print("5. Exit")

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
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
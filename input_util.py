from task import Task


def get_tasks_from_file(file='tasks.txt'):
    with open(file, 'r') as f:
        f.readline()

        tasks = []
        task_num = 1
        while True:
            line = f.readline().split()
            if len(line) == 0:
                break
            tasks.append(Task(task_num, *map(int, line)))
            task_num += 1

        return tasks

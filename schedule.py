from functools import cmp_to_key
from comparator import *
from input_util import *


def is_exist(queue, task):
    return any(task == existed_task for existed_task in queue)


def run():
    tasks = get_tasks_from_file()
    core_M = 1  # num of cores
    sim_time = 1000

    queue_a = []
    queue_u = []
    queue_nu = []

    cur_time = 0
    while cur_time <= sim_time:
        for task in tasks:
            if cur_time % task.P == 0:
                if task.is_urgent():
                    if not is_exist(queue_u, task):
                        queue_u.append(task)
                else:
                    if not is_exist(queue_nu, task):
                        queue_nu.append(task)

                U = 0
                for a_task in queue_a:
                    U += a_task.util

                queue_u.sort(key=cmp_to_key(compare_by_util))
                queue_nu.sort(key=cmp_to_key(compare_by_dis))

                for i in range(len(queue_u)):
                    task = queue_u.pop(0)
                    if U + task.util <= core_M:
                        U += task.util
                        task.init_period(cur_time)
                        queue_a.append(task)
                    else:
                        queue_u.append(task)
                        print("{}에 task{}에 대해서 Dynamic Failure 발생".format(cur_time + 1, queue_u[i].num))

                for i in range(len(queue_nu)):
                    task = queue_nu.pop(0)
                    if U + task.util <= core_M:
                        U += task.util
                        task.init_period(cur_time)
                        queue_a.append(task)
                    else:
                        queue_nu.append(task)

        # P-fair Scheduling
        for task in queue_a:
            task.update_lag(cur_time)

        queue_a.sort(key=cmp_to_key(compare_by_lag))

        for i in range(core_M):
            if len(queue_a) == 0:
                break

            task = queue_a.pop(0)
            task.execute()
            print("{}부터 {}까지 task{} 실행됨".format(cur_time, cur_time + 1, task.num))

            if task.is_end_period(cur_time):
                task.update_dist(task.is_deadline_meet())
            else:
                queue_a.append(task)

        cur_time += 1

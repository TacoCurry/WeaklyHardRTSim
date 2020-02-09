from functools import cmp_to_key

from comparator import *
from input_util import *


def is_exist(queue, task):
    return any(task == existed_task for existed_task in queue)


def is_exist_delete(queue, task):
    for i, existed_task in enumerate(queue):
        if existed_task == task:
            queue.pop(i)
            return


def run():
    tasks = get_tasks_from_file()
    core_M = 1  # num of cores
    sim_time = 1000

    queue_a = []
    queue_u = []
    queue_nu = []

    cur_time = 0
    while cur_time < sim_time:
        for task in tasks:
            if cur_time % task.P == 0:
                task.update_dist(task.is_deadline_meet())
                task.init_period(cur_time)

                if task.is_urgent():
                    if not is_exist(queue_u, task):
                        queue_u.append(task)
                    is_exist_delete(queue_nu, task)
                else:
                    if not is_exist(queue_nu, task):
                        queue_nu.append(task)
                    is_exist_delete(queue_u, task)

                U = 0
                for a_task in queue_a:
                    U += a_task.util

                queue_u.sort(key=cmp_to_key(compare_by_util))
                queue_nu.sort(key=cmp_to_key(compare_by_dis))

                for i in range(len(queue_u)):
                    task = queue_u.pop(0)
                    if U + task.util <= core_M:
                        U += task.util
                        queue_a.append(task)
                    else:
                        queue_u.append(task)
                        print("{}에 task{}에 대해서 Dynamic Failure 발생".format(cur_time + 1, queue_u[i].num))

                for i in range(len(queue_nu)):
                    task = queue_nu.pop(0)
                    if U + task.util <= core_M:
                        U += task.util
                        queue_a.append(task)
                    else:
                        queue_nu.append(task)

        # P-fair Scheduling
        # 1. lag를 업데이트 하고, lag가 큰 순으로 정렬(일단 이렇게 했는데 PD2? 그 알고리즘으로 바꿔야할 것 같아요)
        for task in queue_a:
            task.update_lag(cur_time)
        queue_a.sort(key=cmp_to_key(compare_by_lag))

        # 3. 코어의 개수만큼의 태스크 실행
        cur_time += 1
        for i in range(core_M):
            if i == len(queue_a):
                break
            queue_a[i].execute()
            print("{}부터 {}까지 task{} 실행됨".format(cur_time - 1, cur_time, queue_a[i].num))

        # 4. 주기 끝난 태스크 내보내기
        for i in range(len(queue_a)-1, -1, -1):
            if queue_a[i].is_end_period(cur_time):
                queue_a.pop(i)

    # Print result
    with open('history.txt', 'w') as f:
        f.write("----------\nDeadline\nmeet = 1\nmiss = 0\n----------\n")
        for task in tasks:
            f.write("{}: ".format(task))
            f.write(' '.join(map(str, task.histories[task.k:])))
            f.write('\n')

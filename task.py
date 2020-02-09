"""
Deadline
M = meet = 1 = True
m = miss = 0 = False
"""
deadline_dict = {True: 1, False: 0}


class Task:
    def __init__(self, num, C, P, m, k):
        self.num = num
        self.C = C
        self.P = P
        self.m = m
        self.k = k

        self.util = C / P
        self.dist = 1
        self.lag = self.start_time = 0
        self.S = C
        self.histories = [1 for _ in range(k-1)]

    def update_dist(self, is_meet_deadline):
        # Update histories and count
        self.histories.append(deadline_dict[is_meet_deadline])

        # Calculate and update dist
        count_meet = sum(self.histories[-self.k:])
        dist = 0
        for start in range(-self.k, 0):
            count_meet -= self.histories[start]
            dist += 1
            if count_meet < self.m:
                break
        self.dist = dist

    def is_urgent(self):
        return self.dist == 1

    def update_lag(self, time):
        self.lag = abs((time - self.start_time) * (self.C / self.P) - self.S)

    def init_period(self, time):
        self.lag = self.S = 0
        self.start_time = time

    def execute(self):
        self.S += 1

    def is_end_period(self, time):
        return (self.start_time + self.P) <= time or self.S >= self.C

    def is_deadline_meet(self):
        return self.S >= self.C

    def __str__(self):
        return "Task{}(C={}, P={}, m={}, k={})"\
            .format(self.num, self.C, self.P, self.m, self.k)

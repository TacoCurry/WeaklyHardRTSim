# 데드라인 충족 여부
DEFAULT, m, M = range(3)


class Task:
    def __init__(self, num, C, P, m, k):
        self.num = num
        self.C = C
        self.P = P
        self.m = m
        self.k = k

        self.util = C * m / (P * k)
        self.dist = 1
        self.lag = self.S = self.start_time = 0

        '''
        dynamic failure 판단을 위해 과거 k개 job의 데드라인 충족 여부를 histories에 유지.
        circular queue를 사용.
        '''
        self.histories = [DEFAULT for i in range(k)]
        self.end = DEFAULT

    def update_dist(self, is_meet_deadline):
        # Update histories and count
        self.end = (self.end + 1) % self.k
        if is_meet_deadline:
            self.histories[self.end] = M
        else:
            self.histories[self.end] = m

        # Calculate and update dist
        count_M = 0
        for state in self.histories:
            if state == M:
                count_M += 1

        start = (self.end + 1) % self.k
        dist = 1
        for i in range(self.k):
            if self.histories[start] == M:
                count_M -= 1
            if count_M < m:
                break
            start = (start + 1) % self.k
        self.dist = dist

    def is_urgent(self):
        return self.dist == 1

    def update_lag(self, time):
        self.lag = (time - self.start_time) * (self.C / self.P) - self.S

    def init_period(self, time):
        self.lag = self.S = 0
        self.start_time = time

    def execute(self):
        self.S += 1

    def is_end_period(self, time):
        return (self.start_time + self.P) <= time or self.S >= self.C

    def is_deadline_meet(self):
        return self.S >= self.C

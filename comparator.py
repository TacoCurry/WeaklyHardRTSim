def compare_by_util(x, y):
    return x.util - y.util


def compare_by_dis(x, y):
    return x.dis - y.dis


def compare_by_lag(x, y):
    return y.lag - x.lag

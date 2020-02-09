def compare_by_util(x, y):
    return x.util - y.util


def compare_by_dis(x, y):
    return x.dist - y.dist


def compare_by_lag(x, y):
    return y.lag - x.lag

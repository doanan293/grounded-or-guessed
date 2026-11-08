def f(x):
    y = x * 2
    if x > 100:
        return y
    if x < -100:
        return -1
    return y - 1 if x == 3 else y

import random


def rand_tuples(_min, _max, tuple_len=2, tuple_num=1):
    if tuple_num == 1:
        return tuple(random.randint(_min, _max) for i in range(tuple_len))
    elif tuple_num >= 2:
        return tuple(tuple(random.randint(_min, _max) for j in range(tuple_len)) for i in range(tuple_num))
    else:
        return None


def rand_2d_point(x_min, x_max, y_min, y_max, n=1):
    if n == 1:
        return random.randint(x_min, x_max), random.randint(y_min, y_max)
    elif n >= 2:
        return tuple((random.randint(x_min, x_max), random.randint(y_min, y_max)) for i in range(n))
    else:
        return None
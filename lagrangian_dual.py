import math
import time


def budget(x,m,p):
    if len(p) != len(x):
        raise IndexError('dim(x) not equal to dim(p)')

    items = [p[i]*x[i] for i in range(len(x))]
    return sum(items)

def cobbDouglas(x,u,t):
    if len(t) != len(x):
        raise IndexError('dim(x) not equal to dim(t)')

    items = [x[i]**t[i] for i in range(len(x))]
    return math.prod(items)
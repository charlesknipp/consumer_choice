import math
import time


# calculate the Lagrange Dual for a consumer choice problem with two goods
# and Cobb-Douglas preferences

def budget(x,p,**kwargs):
    if len(p) < len(x):
        raise IndexError('more goods than prices')

    items = [p[i]*x[i] for i in range(len(x))]
    m = kwargs.get('m',None)

    if (m == None) & (len(p) == len(x)):
        return sum(items)

    return ((m-p[0]*x[0])/p[1])


def utility(x,pp,**kwargs):
    if len(pp) < len(x):
        raise IndexError('more goods than preference parameters')

    items = [x[i]**pp[i] for i in range(len(x))]
    u = kwargs.get('u',None)

    if (u == None) & (len(pp) == len(x)):
        return math.prod(items)

    return (u*x[0]**(-pp[0]))**(1/pp[1])


# t = (prices,expenditures)?
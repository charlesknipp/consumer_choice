import math

'''
Now I want to find a way of cumputing the fixed point in the findIntersection
function by using increasing differences, but I'm not too sure on how to ap-
proach that computationally. Additionally I don't know how efficient it will be
over my current algorithm
'''

# define static characteristics price and taste

p = [2,3]
t = [.3,.7]

# define an upper and lower value for variable x

x_l,x_h = 10,20

# theta serves as a general parameter for the given function
# more for a future proof than anything currently useful

def f(x,theta=p):
    items = [x[i]*theta[i] for i in range(len(x))]
    return sum(items)


def g(x,theta=t):
    items = [x[i]**theta[i] for i in range(len(x))]
    return math.prod(items)


# write a function to show IDs holds for a given pair (x_h, x_l)

def isID(func):
    lhs = func([x_h,x_h]) - func([x_l,x_h])
    rhs = func([x_h,x_l]) - func([x_l,x_l])

    if lhs >= rhs:
        print('increasing differences holds for %s(x)' % func.__name__)
        print(round(lhs),'>',round(rhs))
        return True


# returns a boolean value for both f(x) and g(x)

[isID(i) for i in [f,g]]
import math
import time


# calculate the Lagrange Dual for a consumer choice problem with two goods
# and Cobb-Douglas preferences

def budget(x,p):
    return sum([x[i]*p[i] for i in range(len(x))])


def utility(x,pp):
    return math.prod([x[i]**pp[i] for i in range(len(x))])

pp = [.3,.7]
m = 100
p = [3,2]
n = len(p)
error = 3
k = (10**(-error))

x = [(n**(-1))*m/p[i] for i in range(len(p))]
u = utility(x,pp)

def findLambda(x1):
    x2 = [i+k for i in x1]
    xs = []

    # duplicate bundle x, n times, perturbing an element each iteration

    for i in range(n):
        l = []
        for j in range(n):
            if i != j:
                l.append(x1[j])
            else:
                l.append(x2[j])
        xs.append(l)

    return [((utility(xs[i],pp)-utility(x1,pp))/k)/p[i] for i in range(n)]

# the goal is to identify the point where the dual and primal solutions are equal
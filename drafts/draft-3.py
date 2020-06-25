import math
import time


# assuming differentiability, exploit the lagrange version via minimax

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


def adjust(lb,ub):
    x = (lb + ub)/2
    return x


min_x = [0,0]
max_x = [m/p[0],m/p[1]]

its = findLambda(x)
counter = 0

while True:
    if its[1] - its[0] < .00001:
        max_x[1] = x[1]
        min_x[0] = x[0]
        x[1] = adjust(min_x[1],max_x[1])
        x[0] = (m-p[1]*x[1])/p[0]
    
    elif its[0] - its[1] < .00001:
        max_x[0] = x[0]
        min_x[1] = x[1]
        x[0] = adjust(min_x[0],max_x[0])
        x[1] = (m-p[0]*x[0])/p[1]

    else:
        break

    if counter == 100:
        break

    counter += 1
    its = findLambda(x)

print('bundle\t(%.3f,%.3f)' % (x[0],x[1]))
print('lambda\t(%.5f,%.5f)' % (its[0],its[1]))
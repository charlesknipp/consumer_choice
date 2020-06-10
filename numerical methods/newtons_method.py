import math
import time

# requires some notion of differentiability by the limit definition

m = 100
a, b = .3, .7
p = [3,2]

u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

def I(x1,utl):
    return (utl*x1**(-a))**(1/b)

def B(x1,inc):
    return ((inc-p[0]*x1)/p[1])

def intersection(x1,inc,utl):
    return (utl*x1**(-a))**(1/b) - ((inc-p[0]*x1)/p[1])


def derive(value):
    h = 0.0001
    top = intersection(value+h,m,u) - intersection(value,m,u)
    bottom = h
    slope = top / bottom
    return slope


def newtonsMethod(x0,max_iters=20):
    xn = x0
    for n in range(0,max_iters):
        fxn = intersection(xn,m,u)
        if abs(fxn) < .0001:
            return xn
        Dfxn = derive(xn)
        if Dfxn == 0:
            print('Zero derivative. No intersection found.')
            return None
        xn = xn - fxn/Dfxn
    print('Exceeded',n,'iterations. No intersection found.')
    return None

start_time = time.time()
intr = [newtonsMethod(.0001),newtonsMethod(m/p[0])]
elapsed_time = time.time() - start_time

print(intr)
print(B(intr[0],m))
print('time:\t%.3f ms' % (elapsed_time*1000))
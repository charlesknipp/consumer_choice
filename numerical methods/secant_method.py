import math
import time

# the new goal is to define a smart way to predict the bounds where one is above
# and one below the intersection points

m = 100
a, b = .3, .7
p = [3,2]

u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

def I(x1,utl):
    return (utl*x1**(-a))**(1/b)

def B(x1,inc):
    return ((inc-p[0]*x1)/p[1])

def intersection(x1,inc=m,utl=u):
    return (utl*x1**(-a))**(1/b) - ((inc-p[0]*x1)/p[1])

# this is my now preferred numerical method since we have no need for different-
# iablity along equivalence classes

def secantMethod(x1, x2, E=.00001): 
    n,c = 0,0
    xm,x0 = 0,0

    while True:
        top_x0 = x1*intersection(x2) - x2*intersection(x1)
        bottom_x0 = intersection(x2) - intersection(x1)
        x0 = top_x0 / bottom_x0

        c = intersection(x1) * intersection(x0)
        x1,x2 = x2,x0  
        n += 1

        if (c == 0):  
            break

        top_xm = x1*intersection(x2) - x2*intersection(x1)
        bottom_xm = intersection(x2) - intersection(x1)
        xm = top_xm / bottom_xm
        
        if(abs(xm - x0) < E): 
            break

    return x0


start_time = time.time()
intr = secantMethod(.001,.1)
elapsed_time = time.time() - start_time

print('initial guess: (%.5f, %.5f)' % (.5*m/p[0],.5*m/p[1]))
print(intr)
print('time:\t%.3f ms' % (elapsed_time*1000))
import math
import time


m = 100
a, b = .3, .7
p = [3,2]

u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

def I(x1,utl):
    return (utl*x1**(-a))**(1/b)

def B(x1,inc):
    return ((inc-p[0]*x1)/p[1])


def findIntersection(utility):

    def findMin(x,k):
        min_f = abs(I(x[0],utility) - B(x[0],m))
        min_x = x[0]

        for i in x:
            diff = I(i,utility) - B(i,m)
            next_diff = I(i+k,utility) - B(i+k,m)
            if diff < min_f:
                min_f = abs(diff)
                min_x = i-k
                if abs(diff) <= abs(next_diff):
                    break

        return min_x

    def findMax(x,k):
        max_f = abs(I(x[-1],utility) - B(x[-1],m))
        max_x = x[-1]

        for i in list(reversed(x)):
            diff = I(i,utility) - B(i,m)
            prev_diff = I(i-k,utility) - B(i-k,m)
            if diff < max_f:
                max_f = abs(diff)
                max_x = i-k
                if abs(diff) <= abs(prev_diff):
                    break

        return max_x


    n = 3
    x = range(1,math.floor(m/p[0])+1)

    min_x = [findMin(x,1)]
    max_x = [findMax(x,1)]

    for i in range(1,n+1):
        k = 10**(-i)
        mnx = [round(min_x[-1]+j*(k),i) for j in range(0,20)]
        mxx = [round(max_x[-1]+j*(k),i) for j in range(0,20)]

        min_x.append(findMin(mnx,k))
        max_x.append(findMax(mxx,k))

    final_min = min_x[-1]
    final_max = max_x[-1]

    bds = [final_min,final_max]
    return bds

start_time = time.time()
intr = findIntersection(u)
elapsed_time = time.time() - start_time

print(intr)
print('time:\t%.3f ms' % (elapsed_time*1000))
import time
import math


# benchmark this algorithm by asserting a bunch of different cases...eventually
# not currently working

def marshellianDemand(income,preferences,prices):
    m = income
    p = prices

    def utility(x1,x2):
        return 5*x1+3*x2
    
    u = utility(
        (.5*m/p[0]),
        (.5*m/p[1])
    )

    def U(x1,utl):
        return (utl-5*x1)/3


    def B(x1,inc):
        return ((inc-p[0]*x1)/p[1])


    def findIntersection(utility):

        def findMin(x,k):
            min_f = abs(U(x[0],utility) - B(x[0],m))
            min_x = x[0]

            for i in x:
                diff = U(i,utility) - B(i,m)
                next_diff = U(i+k,utility) - B(i+k,m)
                if diff < min_f:
                    min_f = abs(diff)
                    min_x = i-k
                    if abs(diff) <= abs(next_diff):
                        break

            return min_x

        def findMax(x,k):
            max_f = abs(U(x[-1],utility) - B(x[-1],m))
            max_x = x[-1]

            for i in list(reversed(x)):
                diff = U(i,utility) - B(i,m)
                prev_diff = U(i-k,utility) - B(i-k,m)
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


    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = B(x1,m)

        return utility(x1,x2)


    bounds = findIntersection(u)

    while True:
        if abs(bounds[1] - bounds[0]) > .001:
            u = adjust(bounds[0],bounds[1])
        else:
            break
        bounds = findIntersection(u)

    bundle = (bounds[0],U(bounds[0],u))

    return bundle

start_time = time.time()
bundle = marshellianDemand(9,[1,1],[1,1])
elapsed_time = time.time() - start_time

print('bundle:\t(%.2f,%.2f)' % bundle)
print('time:\t%.3f ms' % (elapsed_time*1000))
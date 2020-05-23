import time
import math


# this version uses the linear combination of values along an equivalence class,
# which are constrained to a sublattice valued budget set.

def hicksianDemand(utility,preferences,prices):
    '''
    computes an optimal bundle given a convex constraint and a linear objective, 
    in the context of consumer theory; this particular instance limits the user 
    to a Cobb-Douglas utility function, but can easily be expanded to more 
    general expressions.

    parameters:
        utility (int): the level of indifference represented by the preference 
        relation on the positive reals
        preferences (array): an array of taste parameters that applies to 
        utility
        prices (array): an array containing the prices of good 1 and good 2

    returns:
        bundle (tuple): the optimal bundle x to maximize expenditure subject to 
        an indifference class
    '''

    a = preferences[0]
    b = preferences[1]
    u = utility
    p = prices

    x_i = [u**(1/(a+b)),u**(1/(a+b))]
    m = sum([x_i[i]*p[i] for i in range(2)])

    def U(x1,utl):
        return (utl*x1**(-a))**(1/b)


    def B(x1,inc):
        return ((inc-p[0]*x1)/p[1])


    def findIntersection(income):
        '''
        Calculates the intersection of two curves using a dynamic step size that 
        finds a lower limit and divides that interval by 10 each time.

        returns:
            bounds (array): structured like (min,max), this array represents the 
            points of intersection of the given curve
        '''

        def findMin(x,k):
            min_f = abs(U(x[0],u) - B(x[0],income))
            min_x = x[0]

            for i in x:
                diff = U(i,u) - B(i,income)
                next_diff = U(i+k,u) - B(i+k,income)
                if diff < min_f:
                    min_f = abs(diff)
                    min_x = i
                    if abs(diff) <= abs(next_diff):
                        break

            return min_x

        # also probably broken
        def findMax(x,k):
            max_f = abs(U(x[-1],u) - B(x[-1],income))
            max_x = x[-1]

            for i in list(reversed(x)):
                diff = U(i+k,u) - B(i+k,income)
                prev_diff = U(i,u) - B(i,income)
                if diff < max_f:
                    max_f = abs(prev_diff)
                    max_x = i
                    if abs(diff) <= abs(prev_diff):
                        break

            return max_x


        n = 3
        x = range(1,math.floor(m/p[0])+1)

        min_x = [findMin(x,1)]
        max_x = [findMax(x,1)]

        for i in range(1,n+1):
            k = 10**(-i)
            mnx = [round(min_x[-1]+j*(k),i) for j in range(0,10)]
            mxx = [round(max_x[-1]+j*(k),i) for j in range(0,10)]

            min_x.append(findMin(mnx,k))
            max_x.append(findMax(mxx,k))

        final_min = min_x[-1]
        final_max = max_x[-1]

        bds = [final_min,final_max]
        return bds


    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = U(x1,u)
        bundle = [x1,x2]

        return sum([bundle[i]*p[i] for i in range(2)])


    bounds = findIntersection(m)

    while True:
        if bounds[1] - bounds[0] > .001:
            m = adjust(bounds[0],bounds[1])
        else:
            break

        bounds = findIntersection(m)

    bundle = (bounds[0],B(bounds[0],m))

    return bundle


start_time = time.time()
bundle = hicksianDemand(24.03519395349548,[.3,.7],[3,2])
elapsed_time = time.time() - start_time

print('bundle:\t(%.2f,%.2f)' % bundle)
print('time:\t%.3f ms' % (elapsed_time*1000))
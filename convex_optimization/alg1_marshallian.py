import time
import math


# this version uses the linear combination of values along an equivalence class,
# which are constrained to a sublattice valued budget set.

def marshellianDemand(income,preferences,prices):
    '''
    computes an optimal bundle given a convex objective and a linear constraint, 
    in the context of consumer theory; this particular instance limits the user 
    to a Cobb-Douglas utility function, but can easily be expanded to more 
    general expressions.

    parameters:
        income (int): the amount of money that the  consumer is constrained to 
        spending
        preferences (array): an array of taste parameters that applies to 
        utility
        prices (array): an array containing the prices of good 1 and good 2

    returns:
        bundle (tuple): the optimal bundle x to maximize utility subject to a 
        budget constraint
    '''

    start_time = time.time()

    a = preferences[0]
    b = preferences[1]
    m = income
    p = prices
    u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

    def U(x1,utl):
        return (utl*x1**(-a))**(1/b)


    def B(x1,inc):
        return ((inc-p[0]*x1)/p[1])


    def findIntersection(utility):
        '''
        Calculates the intersection of two curves using a dynamic step size that 
        finds a lower limit and divides that interval by 10 each time.

        returns:
            bounds (array): structured like (min,max), this array represents the 
            points of intersection of the given curve
        '''

        def findMin(x,k):
            diff_pairs = []

            for i in x:
                diff = U(i,utility) - B(i,m)
                next_diff = U(i+k,utility) - B(i+k,m)

                if diff >= 0 and next_diff < diff:
                    diff_pairs.append((i,diff))
                else:
                    pass

            diff_pairs.sort(key=lambda x: abs(x[1]))
            floor_pair = diff_pairs[0]

            return floor_pair[0]


        def findMax(x,k):
            diff_pairs = []

            for i in x:
                diff = U(i,utility) - B(i,m)
                next_diff = U(i+k,utility) - B(i+k,m)

                if diff <= 0 and next_diff > diff:
                    diff_pairs.append((i,diff))
                else:
                    pass
            
            diff_pairs.sort(key=lambda x: abs(x[1]))
            floor_pair = diff_pairs[0]

            return floor_pair[0]


        n = 3
        x = range(1,math.floor(m/p[0])+1)

        min_x = [findMin(x,1)]
        max_x = [findMax(x,1)]

        for i in range(1,n+2):
            k = 10**(-i)
            mnx = [round(min_x[-1]+j*(k),i) for j in range(0,10)]
            mxx = [round(max_x[-1]+j*(k),i) for j in range(0,10)]

            min_x.append(findMin(mnx,k))
            max_x.append(findMax(mxx,k))

        final_min = round(min_x[-1],n)
        final_max = round(max_x[-1],n)

        bds = [final_min,final_max]
        return bds


    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = B(x1,m)
        utility = ((x1)**a)*((x2))**(b)

        return utility


    bounds = findIntersection(u)

    while True:
        if abs(bounds[1] - bounds[0]) > .001:
            u = adjust(bounds[0],bounds[1])
        else:
            break
        bounds = findIntersection(u)

    bundle = (bounds[0],U(bounds[0],u))
    elapsed_time = time.time() - start_time

    return [bundle,elapsed_time]


v = marshellianDemand(100,[.3,.7],[3,2])
bundle = v[0]
time = v[1]


print('bundle:\t(%.2f,%.2f)' % v[0])
print('time:\t%.3f microseconds' % (v[1]*1000))
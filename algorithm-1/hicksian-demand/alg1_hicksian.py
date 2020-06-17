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


    def findIntersection(inc):
        '''
        Calculates the intersection of two curves using a dynamic step size that 
        finds a lower limit and divides that interval by 10 each time.

        returns:
            bounds (array): structured like (min,max), this array represents the 
            points of intersection of the given curve
        '''

        def intersection(x1):
            return (u*x1**(-a))**(1/b) - ((inc-p[0]*x1)/p[1])


        def derive(value):
            h = .0000001
            top = intersection(value+h) - intersection(value)
            bottom = h
            slope = top / bottom
            return slope


        def newtonsMethod(x0,max_iters=30):
            xn = x0
            for n in range(0,max_iters):
                fxn = intersection(xn)
                if abs(fxn) < .00000001:
                    return xn
                Dfxn = derive(xn)
                if Dfxn == 0:
                    print('Zero derivative. No intersection found.')
                    return None
                xn = xn - fxn/Dfxn
            print('Exceeded',n,'iterations. No intersection found.')
            return None

        bds = [newtonsMethod(.0001),newtonsMethod(m/p[0])]
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
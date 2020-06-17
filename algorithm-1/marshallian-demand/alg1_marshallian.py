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

    a = preferences[0]
    b = preferences[1]
    m = income
    p = prices
    
    u = ((.5*m/p[0])**a)*((.5*m/p[1]))**(b)

    def U(x1,utl):
        return (utl*x1**(-a))**(1/b)


    def B(x1,inc):
        return ((inc-p[0]*x1)/p[1])


    def findIntersection(utl):
        '''
        Calculates the intersection of two curves using a dynamic step size that 
        finds a lower limit and divides that interval by 10 each time.

        returns:
            bounds (array): structured like (min,max), this array represents the 
            points of intersection of the given curve
        '''

        def intersection(x1):
            return (utl*x1**(-a))**(1/b) - ((m-p[0]*x1)/p[1])


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
                if abs(fxn) < .0000001:
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
    return bundle

start_time = time.time()
bundle = marshellianDemand(9,[1,1],[1,1])
elapsed_time = time.time() - start_time

print('bundle:\t(%.2f,%.2f)' % bundle)
print('time:\t%.3f ms' % (elapsed_time*1000))
import math
import time

# Work in progress!!!! Not finished

def B(x1,income,prices):
    '''
    parameters:
        x1 (float): any amount of good 1
        income (float): a level of income m
        prices (array): a vector of prices (p1,p2)
    returns:
        x2 (float): an amount of good 2 that fits within the given budget
    '''

    p = prices
    m = income

    return ((m-p[0]*x1)/p[1])


def U(x1,utility,preferences):
    '''
    parameters:
        x1 (float): any amount of good 1
        utility (float): a given level of indifference
        preferences (array): a vector of parameters per each good (a,b)

    returns:
        x2 (float): a value for good 2 that keeps the consumer indifferent
    '''

    u = utility
    a = preferences[0]
    b = preferences[1]
    
    return (u*x1**(-a))**(1/b)


# the only problem I have with this algorithm is the use of the mean value, but
# I don't have an alternative especially since using the Marshallian case is
# far more computationally intensive

def hicksianCase(utility,preferences,prices,precision=3):
    '''
    computes the optimal bundle given a level of indifference between two goods

    parameters:
        utility (int): the constrained level of indifference
        preferences (array): an array of taste parameters that applies to
        utility
        prices (array): an array containing the prices of good 1 and good 2
        precision (int): the power representing the decimal place of accuracy

    returns:
        bundle (tuple): the optimal bundle of x to minimize expenditures subject
        to utility
    '''

    k1 = 10**precision
    k2 = 1/k1
    a = preferences[0]
    b = preferences[1]
    u = utility
    x_i = [u**(1/(a+b)),u**(1/(a+b))]
    p = prices
    m = sum([x_i[i]*p[i] for i in range(2)])


    def findIntersection(x,income):
        min_f = abs(U(x[0],u,[a,b]) - B(x[0],income,p))
        max_f = abs(U(x[-1],u,[a,b]) - B(x[-1],income,p))
        min_x = x[0]
        max_x = x[-1]
        for i in x:
            diff = U(i,u,[a,b]) - B(i,income,p)
            next_diff = U(i+k2,u,[a,b]) - B(i+k2,income,p)
            if diff < min_f:
                min_f = abs(diff)
                min_x = i
                if abs(diff) <= abs(next_diff):
                    break

        for i in list(reversed(x)):
            diff = U(i,u,[a,b]) - B(i,income,p)
            prev_diff = U(i-k2,u,[a,b]) - B(i-k2,income,p)
            if diff < max_f:
                max_f = abs(diff)
                max_x = i
                if abs(diff) <= abs(prev_diff):
                    break

        bds = [min_x,max_x]
        return bds

    # adjust the selection to a supermodular euclidean higher selection on B()
    # solve the Hicksian case first then use that to converge to a Marshallian
    # solution?

    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = U(x1,u,[a,b])
        bundle = [x1,x2]
        budget = sum([bundle[i]*p[i] for i in range(2)])

        return budget

    x = [round(x*k2,precision) for x in range(1,math.ceil(m/p[0])*k1+1)]

    bounds = findIntersection(x,m)
    iters = [m]

    while True:
        if bounds[1] - bounds[0] > k2:
            m = adjust(bounds[0],bounds[1])
            iters.append(m)
        else:
            break
        bounds = findIntersection(x,m)

    bundle = (bounds[0],B(bounds[0],m,p))

    return bundle


start_time = time.time()

ui = []
n = 2
ctr = 0

p = [3,2]
t = [.3,.7]
m = 100

xi = [(n**(-1))*m/p[i] for i in range(n)]
ui.append(math.prod([xi[i]**t[i] for i in range(n)]))

while True:
    z = hicksianCase(ui[-1],t,p)
    zi = (z[0],B(z[0],m,p))
    ui.append(math.prod([zi[i]**t[i] for i in range(n)]))

    if m-sum([z[i]*p[i] for i in range(n)]) < .00001:
        break

elapsed_time = time.time() - start_time
print(hicksianCase(ui[-2],t,p))
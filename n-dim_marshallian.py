import math
import time
from tqdm import tqdm


# for when I do decide to take this case in n dimensions use these functions
'''
def budgetSet(x,p,m):
    e_n = [x[i]*p[i] for i in range(n-1)]
    return (m-sum(e_n))/p[-1]


def utilitySet(x,t,u):
    b_n = [x[i]**t[i] for i in range(n-1)] 
    return (u*math.prod(b_n))**(1/t[-1])
'''

# use these ones for now, it's easier to keep track
def budget(x1,income,prices):
    p = prices
    m = income

    return ((m-p[0]*x1)/p[1])


def indifference(x1,utility,preferences):
    u = utility
    a = preferences[0]
    b = preferences[1]
    
    return (u*x1**(-a))**(1/b)


# until then, just use the ones I designed in the previous algorithm
t = [.3,.5,.2]
p = [5,3,2]
m = 100
n = 3

# set error bounds for the fixed point approximation
k = 3
k1 = 10**k
k2 = 10**(-k)

# accept an initial guess for x_3 by dividing our budget into 3 slices
x1 = [(n**(-1))*m/p[i] for i in range(n)]

# now let m_not be the money we spend on all but x_3 and solve for the bundle
# (x_1,x_2) where x_3 is fixed at m/(3*p_3)

def nIteration(xi,m):
    utility = math.prod([xi[i]**t[i] for i in range(n)])
    u = utility/(xi[-1]**t[-1])
    m = m-p[-1]*xi[-1]

    a = t[0]
    b = t[1]

    def findIntersection(x,utility):
        min_f = abs(indifference(x[0],utility,[a,b]) - budget(x[0],m,p))
        max_f = abs(indifference(x[-1],utility,[a,b]) - budget(x[-1],m,p))
        min_x = x[0]
        max_x = x[-1]
        for i in x:
            diff = indifference(i,utility,[a,b]) - budget(i,m,p)
            next_diff = indifference(i+k2,utility,[a,b]) - budget(i+k2,m,p)
            if diff < min_f:
                min_f = abs(diff)
                min_x = i
                if abs(diff) <= abs(next_diff):
                    break

        for i in list(reversed(x)):
            diff = indifference(i,utility,[a,b]) - budget(i,m,p)
            prev_diff = indifference(i-k2,utility,[a,b]) - budget(i-k2,m,p)
            if diff < max_f:
                max_f = abs(diff)
                max_x = i
                if abs(diff) <= abs(prev_diff):
                    break

        bds = [min_x,max_x]
        return bds


    def adjust(lower_bound,upper_bound):
        x1 = (lower_bound+upper_bound)/2
        x2 = budget(x1,m,p)
        utility = ((x1)**a)*((x2))**(b)

        return utility


    # parameterize x_1 to some variable s
    s = [round(x*k2,k) for x in range(1,math.ceil(m/p[0])*k1+1)]

    bounds = findIntersection(s,u)
    iters = [u]

    while True:
        if bounds[1] - bounds[0] > k2:
            u = adjust(bounds[0],bounds[1])
            iters.append(u)
        else:
            break
        bounds = findIntersection(s,u)

    bundle = [bounds[0],indifference(bounds[0],u,[a,b]),xi[2]]

    return bundle


# come up with some clever way of iterating it over higher dimensions

start_time = time.time()
v = [round(x*.1,2) for x in range(1,math.ceil(m/p[0])*10)]
base = nIteration(x1,m)
max_u = [math.prod([base[i]**t[i] for i in range(n)])]
min_u = math.prod([base[i]**t[i] for i in range(n)])

bundles = [base]

for x in tqdm(v):
    m_not = m-x*p[-1]
    slctn = [m_not/(2*p[i]) for i in range(n-1)]
    slctn.append(x*p[-1])
    bndl = nIteration(slctn,m)
    utl = math.prod([bndl[i]**t[i] for i in range(n)])

    if utl-max_u[-1] > 0:
        max_u.append(utl)
        bundles.append(bndl)

    elif utl-max_u[-1] < 0 & len(bundles) > 10:
        break

    else:
        continue

elapsed_time = time.time() - start_time

print(bundles[-1])
print('%.5f seconds elapsed' % elapsed_time)
import math

# this is the most straight forward of algorithms using a simple sorted dict to
# to find the maximal element, and thus is the least time complex

u = 24.03519395349548
p = [3,2]
t = [.3,.7]

def e(x):
    # defined to reduce the amount of code I need to type
    return sum([x[i]*p[i] for i in range(2)])

# for the hicksian case, the constrained equivalence class is unbounded
xi = [u**(1/(t[0]+t[1])),u**(1/(t[0]+t[1]))]
mi = sum([xi[i]*p[i] for i in range(2)])

# reduce time complexity by performing this operation once
d1 = math.ceil((mi/p[0])*1000)
d2 = d1-1

# uses the sublattice valued budget to substitute for x2
x1 = [round(x/1000,3) for x in range(1,d1)]
x2 = [(u*x1[i]**(-t[0]))**(1/t[1]) for i in range(d2)]

# construct a feasible set and the resulting objective
bundles = [(x1[i],x2[i]) for i in range(d2)]
objectives = [e(i) for i in bundles]

# assigns each coordinate with its respective value function
x = {bundles[i]: objectives[i] for i in range(d2)}

hicksian_set = {
    k: v for k, v in sorted(x.items(),
    key=lambda item: item[1])
}

# prints the bundle with the largest u(x)
print(list(hicksian_set.items())[0])
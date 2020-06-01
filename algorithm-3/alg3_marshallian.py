import math

# this is the most straight forward of algorithms using a simple sorted dict to
# to find the maximal element, and thus is the least time complex

m = 100
p = [3,2]
t = [.3,.7]

def u(x):
    # defined to reduce the amount of code I need to type
    return math.prod([x[i]**t[i] for i in range(2)])


# reduce time complexity by performing this operation once
d1 = math.ceil((m/p[0])*1000)
d2 = d1-1

# uses the sublattice valued budget to substitute for x2
x1 = [round(x/1000,3) for x in range(1,d1)]
x2 = [((m-p[0]*x1[i])/p[1]) for i in range(d2)]

# construct a feasible set and the resulting objective
bundles = [(x1[i],x2[i]) for i in range(d2)]
objectives = [u(i) for i in bundles]

# assigns each coordinate with its respective value function
x = {bundles[i]: objectives[i] for i in range(d2)}

marshallian_set = {
    k: v for k, v in sorted(x.items(),
    key=lambda item: item[1])
}

# prints the bundle with the largest u(x)
print(list(marshallian_set.items())[-1])
# use the normal vector to the budget line
using LinearAlgebra

# define variables now before nesting it in a function
m = 100
p = [3,2]
t = [.3,.7]
n = length(p)

# define the objective function
function utility(x::Array)
    return prod(x.^t)
end

function expenditure(x::Array)
    return sum(p.*x)
end

# define the marginal rate functionally
function marginalUtility(x::Array)
    u_prime = zeros(Float64,n)
    for j in 1:n
        u_prime_args = [i==j ? t[i]*x[i]^(t[i]-1) : x[i]^t[i] for i in 1:n]
        u_prime[j] = prod(u_prime_args)
    end

    return u_prime
end

# define a function for the normal vector to the budget line
function normalBudget(x1::Float64)
    x2 = (100-p[1]*x1)/p[2]
    normal_vector = [x1-p[2],x2-p[2]]

    return normal_vector
end

# finish code later because I am too distracted to finish it now
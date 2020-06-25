# exploit differentiability by using the subgradient

# define variables now before nesting it in a function
m = 100
p = [3 2]
t = [.3 .7]
n = length(p)

# define the objective function
function utility(x::Array)
    return prod(x.^t)
end

function expenditure(x::Array)
    return sum(p.*x)
end


# define the marginal rate via limit definition
function marginalUtilityLimit(x::Array,h::Float64=.001)
    u_prime = zeros(Float64,n)
    x_pert = [[i==j ? x[i]+h : x[i] for i in 1:n] for j in 1:n]
    # not working just yet
    u_prime = [(utility(x_pert[i])-utility(x)) / h for i in 1:n]

    return u_prime
end

# define the marginal rate functionally, needs improvement
function marginalUtility(x::Array)
    u1_prime = t[1]*x[1]^(t[1]-1) * x[2]^t[2]
    u2_prime = x[1]^t[1] * t[2]*x[2]^(t[2]-1)

    return [u1_prime u2_prime]
end


# define the adjustment to reach an optimal point
function adjust(x::Array)
    budget = [m/p[1] m/p[2]]
    grad = marginalUtility(x)

    # calculate the projection onto the budget line
    norm = sum(budget.*budget)
    dot = sum(budget.*grad)
    proj = dot/(norm^2) * budget

    return x .+ proj
end

println(marginalUtility([10.0 35.0]))
println(marginalUtilityLimit([10.0 35.0]))

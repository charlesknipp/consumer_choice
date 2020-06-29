#=
    unfortunately this one does not seem to work

    for some reason or another the gradient vector at the optimal point is not
    perpendicular to the budget line and therefore the projection onto the line
    perturbs what should have been the optimal solution

    try something with the normal vector to the budget line and that might war-
    rant some useful results, and may transform this problem into a least
    squares problem with enough work
=#

# exploit differentiability by using the subgradient
using LinearAlgebra
using Plots

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


# define the marginal rate via limit definition
function marginalUtilityLimit(x::Array,h::Float64=.001)
    u_prime = zeros(Float64,n)
    x_pert  = [[i==j ? x[i]+h : x[i] for i in 1:n] for j in 1:n]
    u_prime = [(utility(x_pert[i])-utility(x)) / h for i in 1:n]

    return u_prime
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


# define the adjustment to reach an optimal point
function adjust(x::Array)
    budget = [m/p[1],m/p[2]]
    grad = marginalUtility(x) .+ x

    # calculate the projection onto the budget line
    norm = sum(budget.*budget)
    dot = sum(budget.*grad)
    proj = dot/(norm^2) * budget

    return x .+ proj
end

# define an initial guess
x_initial = [(1/n)*m/p[i] for i in 1:n]


# for graphing and testing purposes...
function utilityGraph(x1::Float64)
    utl = utility(x_initial)
    return (utl*x1^(-t[1]))^(1/t[2])
end

function budgetGraph(x1::Float64)
    (m-x1*p[1])/p[2]
end

# define the vector in cartesian form
mu1 = marginalUtility(x_initial)
x1i = [x_initial[1],mu1[1]+x_initial[1]]
x2i = [x_initial[2],mu1[2]+x_initial[2]]

mu2 = marginalUtility([10,35])
x1o = [10,mu1[1]+10]
x2o = [35,mu2[2]+35]

plt1 = plot(utilityGraph,5,20,aspect_ratio=:equal)
plot!(budgetGraph,5,20)
plot!(x1i,x2i)
plot!(x1o,x2o)
display(plt1)
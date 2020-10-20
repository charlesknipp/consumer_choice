using Plots
using Printf

# normalized prices wrt x
p = 1
m = 20

# set a random variable for y in order to minimax on the non-composite good
x_not = (m/p)*rand(Float64)
x_not = 10

begin
    # define prefereces and constraints to construct a Lagrangian
    u(x,y) = (x^.5)*(y^.5)
    Γ(x) = (m-x)/p
    L(x,λ,y=x_not) = u(x,y)+λ*(m-x-y*p)
end

# define ranges for all inputs and construct a series from these conditions
X = 0:.04:m
Y = 0:.04:(m/p)
λ = 0.01:.01:1


# plot the values using the GR backend
plt = plot(surface(X,(0:.01:1),L,camera=(80,60),fillcolor=:viridis))

# use single crossing definition to keep it discrete
function isSupermodular(high::Tuple,low::Tuple)
    x_l,y_l = low
    x_h,y_h = high

    sm = u(x_h,y_h)-u(x_l,y_h) >= u(x_h,y_l)-u(x_l,y_l) ?  true : false
    return sm
end


# try to animate the plot for some minimax type argument
function maxmin(y)
    lagrange_inf_space = []
    λ_indices = []

    for x in X
        min_search_region = [L(x,λ_i,y) for λ_i in λ]
        lagrange_inf,λ_index = findmin(min_search_region)

        # put these values into the local scope, so we can maximize
        push!(lagrange_inf_space,lagrange_inf)
        push!(λ_indices,λ_index)
    end

    lagrange_sup,x_index = findmax(lagrange_inf_space)

    return lagrange_sup,X[x_index]
end


function minimax(y)
    lagrange_sup_space = []
    x_indices = []

    for λ_i in λ
        max_search_region = [L(x,λ_i,y) for x in X]
        lagrange_sup,x_index = findmax(max_search_region)

        # put these values into the local scope, so we can minimize
        push!(lagrange_sup_space,lagrange_sup)
        push!(x_indices,x_index)
    end

    lagrange_inf,λ_index = findmin(lagrange_sup_space)

    return lagrange_inf,X[x_indices[λ_index]]
end

if minimax(10) == maxmin(10)
    x_optimum = maxmin(10)
    @printf("zero duality holds and x* = %.2f",x_optimum[2])
end
using LinearAlgebra

# for a consumer choice problem, let's switch to a vector space real quick
struct FeasibleBundles
    prices::AbstractVector
    income::Float64
end

pareto_weights = [.3,.7]
f(x::Vector) = pareto_weights'*([log(xᵢ) for xᵢ in x])

# f is concave iff f(y) ≥ f(x) + g'(y-x) ∀x,y s.t. g = ∇f(⋅)
function subgradient(x::Vector,step::Float64=.00001)
    ∇f = []

    for i = 1:length(x)
        x_prime = copy(x)
        x_prime[i] += step
        push!(∇f, (f(x_prime)-f(x))/step)
    end

    return ∇f
end

# subgradient method: x^(k+1) = x^(k) - αₖ*g^(k)
function subgradientMethod(x₀::Vector,iters::Integer=50)
    f_best = 0.0
    x_k = x₀

    for i=1:iters
        α_k = 1/sqrt(i)             # use the Quake III algorithm to calculate
        ∇f_k = subgradient(x_k)
        x_k -= α_k*∇f_k
        best = max(f_best,f(x_k))
    end

    return f_best
end

# use the unit normal vector to identify an optimal bundle given inada condns.
function unitNormalMethod()
end

# simple Newton Method used in some other code of mine
function newtonsMethod(x0::Number, maxiter::Integer=50, step::Float64=.00001)
    for _ in 1:maxiter
        yprime = derive(x0,step)
        if abs(yprime) < 1e-10
            return x0
        end
        y = f(x0)
        x1 = x0 - y/yprime
        if abs(x1-x0) < 1e-8
            return x1
        end
        x0 = x1
    end
    error("Max iteration exceeded")
end
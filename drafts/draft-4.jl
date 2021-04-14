using Base.Iterators
using LinearAlgebra

# just use Cobb-Douglas because it is supermodular in x on X = {x|x∈Rⁿ,α≥0}
α = [.3,.2,.1,.4]
f(x) = reduce(*,x.^α)
lagrange(x,λ) = f(x) + λ*(m-reduce(+,p.*x))

function constraintSet(p::Array,t::Float64,equality::Bool=false,δ::Int=2)
    feasible(x)  = sum(p.*x)-t ≤ 0 ? true : false
    efficient(x) = abs(sum(p.*x)-t) ≤ exp10(-δ) ? true : false

    rnd(pᵢ) = round(t/pᵢ,digits=δ)
    ϵ = exp10(-δ)

    max_vals = [rnd(pᵢ) ≤ t/pᵢ ? rnd(pᵢ) : rnd(pᵢ)-ϵ for pᵢ in p]
    space = vec(collect.(product((0.0:ϵ:max for max in max_vals)...)))

    return equality == true ? filter(efficient,space) : filter(feasible,space)
end


function lineSearch(p::Array,t::Float64,equality::Bool=true)
    global x_optimal
    Γ = constraintSet(p,t,equality)
    x_optimal = Γ[1]
    
    for x in Γ
        if f(x) ≥ f(x_optimal)
            x_optimal = x
        else
            continue
        end
    end
    
    return x_optimal
end

# derive using the limit definition
function subgradient(x::Vector,step::Float64)
    ∇f = []

    for i = 1:length(x)
        x_prime = copy(x)
        x_prime[i] += step
        push!(∇f, (f(x_prime)-f(x))/step)
    end

    return ∇f
end

function gradientAscent(p,t,δ,max_iters=1000)
    n = length(p)
    ϵ = exp10(-δ)

    global xₖ = [t/(n*pᵢ) for pᵢ in p]
    global αₖ = 1

    ∇f(x) = subgradient(x,.00000001)
    proj  = Matrix(1.0I,n,n) - p*inv(p'*p)*p'

    for k in 1:max_iters
        αₖ = .9*αₖ  # this is kinda funky, but it works

        xₖ_prev = xₖ
        xₖ = xₖ_prev + αₖ*(proj*∇f(xₖ_prev))
        # println(xₖ)

        if abs(f(xₖ)-f(xₖ_prev)) ≤ ϵ
            break
        end
    end

    return round.(xₖ,digits=3)
end

# Γ = constraintSet([2.0,2.0,2.0],3.0,false)
# lineSearch(Γ)

p_test = [2.0,2.0,2.0,2.0]
t_test = 3.0

# @time sol1 = lineSearch(p_test,t_test)
@time sol2 = gradientAscent(p_test,t_test,8)
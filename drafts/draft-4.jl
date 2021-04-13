using Base.Iterators

# just use Cobb-Douglas because it is supermodular in c on C = {c|c∈Rⁿ,α≥0}
α = [1.0/3.0,1.0/3.0,1.0/3.0]
f(x) = reduce(*,x.^α)
lagrange(x,λ) = f(x) + λ*(m-reduce(+,p.*x))

# the lagrangian is in terms of a vector, should probably rethink how my data is
# structured

function constraintSet(p::AbstractArray,t::Float64,δ::Int=2)

    feasible(x) = sum(p.*x)-t ≤ 0 ? true : false
    rnd(p_i) = round(t/p_i,digits=δ)
    ϵ = 10.0^(-δ)

    max_vals = [rnd(p_i) ≤ t/p_i ? rnd(p_i) : rnd(p_i)-ϵ for p_i in p]
    space = product((0.0:ϵ:max for max in max_vals)...)
    space = vec(collect.(space))

    return filter(feasible,space)
end

function lineSearch(Γ)
    
    global x_optimal
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

Γ = constraintSet([2.0,2.0,2.0],3.0)
lineSearch(Γ)
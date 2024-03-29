using Base.Iterators
using LinearAlgebra
using BenchmarkTools
using Plots

# Cobb-Douglas with weights α
α = [.3,.7]
f(x::Vector{Float64}) = reduce(*,x.^α)

# quasilinear
# f(x::Vector{Float64}) = x[1]^.5 + x[2]

# perfect complements
# f(x::Vector{Float64}) = min(x[1]/2,x[2])

# almost as inefficient as the binary search itself, but works really well
function constraintSet(p::Vector{Float64},t::Float64,equality::Bool=false,δ::Int64=3)
    feasible(x)  = sum(p.*x)-t ≤ 0 ? true : false
    efficient(x) = abs(sum(p.*x)-t) ≤ exp10(-δ) ? true : false

    rnd(pᵢ) = round(t/pᵢ,digits=δ)
    ϵ = exp10(-δ)

    max_vals = [rnd(pᵢ) ≤ t/pᵢ ? rnd(pᵢ) : rnd(pᵢ)-ϵ for pᵢ in p]
    space = vec(collect.(product((0.0:ϵ:max for max in max_vals)...)))

    return equality == true ? filter(efficient,space) : filter(feasible,space)
end

# the literal worst algorithm epsecially in higher dimensions with dense spaces
function binarySearch(p::Vector{Float64},t::Float64,equality::Bool=false)
    global x_optimal
    Γ = constraintSet(p,t,equality)
    x_optimal = Γ[1]
    
    for x in Γ
        if f(x) ≥ f(x_optimal)
            x_optimal = x
        end
    end
    println(length(Γ))
    return x_optimal
end

# derive using the limit definition
function subgradient(x::Vector{Float64},ϵ::Float64)
    n = length(x)
    ∇f = zeros(n)

    for i = 1:n
        x_plus, x_minus = copy(x), copy(x)
        x_plus[i]  += ϵ

        if x[i]-ϵ >= 0
            x_minus[i] -= ϵ
            ∇f[i] = (f(x_plus)-f(x_minus))/(2*ϵ)
        else
            ∇f[i] = (f(x_plus)-f(x))/ϵ
        end
    end

    return ∇f
end

# there's an issue here with nonsingularity given small enough epsilon values
function hessian(x::Vector{Float64},ϵ::Float64)
    n = length(x)
    H = zeros(n,n)
    xpp,xpm,xmp,xmm = copy(x),copy(x),copy(x),copy(x)

    for i = 1:n
        xi = x[i]
        xpp[i],xmm[i] = xi+ϵ,xi-ϵ

        H[i,i] = (f(xpp)-2*f(x)+f(xmm))/(ϵ*ϵ)

        xp = xi + ϵ
        xm = xi - ϵ

        xpp[i],xpm[i] = xp,xp
        xmp[i],xmm[i] = xm,xm

        for j = i+1:n
            xj = x[j]
            xp = xj + ϵ
            xm = xj - ϵ

            xpp[j],xpm[j] = xp,xm
            xmp[j],xmm[j] = xp,xm

            H[i,j] = (f(xpp)-f(xpm)-f(xmp)+f(xmm))/(4*ϵ*ϵ)

            xpp[j],xpm[j] = xj,xj
            xmp[j],xmm[j] = xj,xj
        end

        xpp[i],xpm[i] = xi,xi
        xmp[i],xmm[i] = xi,xi
    end

    LinearAlgebra.copytri!(H,'U')
end

# performs a gradient ascent on the objective and projects onto the constraint
function projectedGradientAscent(p::Vector{Float64},t::Float64,δ::Int64=8,max_iters::Int64=1000)
    n = length(p)
    ϵ = exp10(-δ)

    global xₖ = [t/(n*pᵢ) for pᵢ in p]
    global xₖ_prev

    path = xₖ
    ∇f(x) = subgradient(x,ϵ)
    proj  = Matrix(1.0I,n,n) - p*inv(p'*p)*p'

    for k in 1:max_iters
        if k == 1
            αₖ = 1
        else
            Δx  = xₖ-xₖ_prev
            ΔDf = ∇f(xₖ)-∇f(xₖ_prev)
            αₖ = abs((Δx⋅ΔDf))/(ΔDf⋅ΔDf)
            # println(αₖ)
        end

        xₖ_prev = xₖ
        Δxₖ = αₖ*(proj*∇f(xₖ_prev))
        xₖ  = xₖ_prev + Δxₖ

        if sum(x->x>=0, xₖ) != n
            xₖ = xₖ_prev + .5*(proj*∇f(xₖ_prev))
        end

        path = hcat(path,xₖ)
        # println(k)
        
        sqrt(dot(Δxₖ,Δxₖ)) ≤ .0001 ? break : continue
    end

    # return path',round.(xₖ,digits=3)
    return xₖ
end

# this operates on the lagrangian rather than the objective function
function lagrangianAscent(p::Vector{Float64},t::Float64,δ::Int64=8,max_iters::Int64=10000)
    n = length(p)
    ϵ = exp10(-δ)

    global xₖ = [t/(n*pᵢ) for pᵢ in p]
    global λₖ = 1.0
    global xₖ_prev

    path = xₖ
    ∇f(x) = subgradient(x,ϵ)
    Hf(x) = hessian(x,.001)

    for k in 1:max_iters
        xₖ_prev = xₖ
        ΔL = [Hf(xₖ) -p; -p' 0.0]\[(-∇f(xₖ)+λₖ*p)' p'*xₖ-t]'
        Δx, Δλ = ΔL[1:n], ΔL[n+1]
        xₖ = abs.(xₖ+Δx)
        λₖ = λₖ+Δλ
        
        # print(k)
        path = hcat(path,xₖ)

        sqrt(dot(ΔL,ΔL)) ≤ .0001 ? break : continue
    end

    # return (round.(xₖ,digits=3),round(λₖ,digits=δ))
    # return (xₖ,λₖ)
    return xₖ
end

# for benchmarking and comparing computational efficiency
p_test4 = [2.0,2.0,2.0,2.0]
p_test3 = [2.0,2.0,2.0]
p_test2 = [1.0,1.0]
t_test = 3.0

# @benchmark binarySearch(p_test2,t_test)
# @benchmark lagrangianAscent(p_test2,t_test)
# @benchmark projectedGradientAscent(p_test2,t_test)

"""
p,x_optimal = projectedGradientAscent(p_test2,t_test)
plot([0,3],[3,0])
scatter!(p[:,1],p[:,2])
"""

println(projectedGradientAscent(p_test2,4.0))
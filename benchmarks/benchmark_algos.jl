using JuMP
using Ipopt

function case1()
    model = Model(with_optimizer(Ipopt.Optimizer))
    @variable(model, x1 >= 0)
    @variable(model, x2 >= 0)
    @variable(model, x3 >= 0)
    @variable(model, x4 >= 0)
    @NLobjective(model, Max, (x1^.3)*(x2^.2)*(x3^.1)*(x4^.4))
    @constraint(model, Γ, 2x1 + 2x2 + 2x3 + 2x4 <= 3)

    optimize!(model)

    @show value(x1)
    @show value(x2)
    @show value(x3)
    @show value(x4)
end

function case2()
    model = Model(with_optimizer(Ipopt.Optimizer))
    @variable(model, x1 >= 0)
    @variable(model, x2 >= 0)

    @NLobjective(model, Max, x1*(x2-1.0)^3 + x1)
    @constraint(model, Γ, x1 + x2 <= 2.93)

    optimize!(model)

    @show value(x1)
    @show value(x2)
    @show dual(Γ)
end
using JuMP
using Ipopt

model = Model(with_optimizer(Ipopt.Optimizer))
@variable(model, x1 >= 0)
@variable(model, x2 >= 0)
@variable(model, x3 >= 0)
@variable(model, x4 >= 0)
@NLobjective(model, Max, (x1^.3)*(x2^.2)*(x3^.1)*(x4^.4))
@constraint(model, Γ, 2x1 + 2x2 + 2x3 + 2x4 <= 3)

@time optimize!(model)

@show value(x1)
@show value(x2)
@show value(x3)
@show value(x4)

# 0.45
# 0.3
# 0.15
# 0.6

# test time      = .017 seconds
# algorithm time = .069 seconds
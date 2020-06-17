# create a system of numerical methods in julia because it's fast as fuck

m = 100
t = [.3 .7]
p = [3 2]

u = ((.5*m/p[1])^t[1])*((.5*m/p[2]))^(t[2])

# mash together the functions into one
function f(x1,utl=u,inc=m)
    I = (utl*x1^(-t[1]))^(1/t[2])
    B = ((inc-p[1]*x1)/p[2])
    return I-B
end

# derive using the limit definition
function derive(x)
    h = .00001
    return (f(x+h) - f(x))/h
end

function newtonsMethod(x0::Number, maxiter::Integer=50)
    for _ in 1:maxiter
        yprime = derive(x0)
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

print(newtonsMethod(.001))

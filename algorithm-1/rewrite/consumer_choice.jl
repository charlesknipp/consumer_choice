# rewrite in Julia because it is faster than Python and easier than Go

function marshallianDemand(m::Number, p::Array, t::Array)

    # define indifference
    function I(utl::Number,x1::Number)
        (utl*x1^(-t[1]))^(1/t[2])
    end

    # define affordability
    function B(x1::Number)
        (m-x1*p[1])/p[2]
    end

    # set initial affordable guess
    u = (.5*(m/p[1]))^(t[1])*(.5*(m/p[2]))^(t[2])

    function findIntersection(utl::Float64)
        function f(x1::Float64)
            I(utl,x1) - B(x1)
        end

        # derive using the limit definition
        function derive(x1::Float64)
            h = .0001
            return (f(x1+h)-f(x1))/h
        end

        function newtonsMethod(x0::Float64,maxiter::Integer=30)
            for _ in 1:maxiter
                yprime = derive(x0)
                if abs(yprime) < 1e-5
                    return x0
                end
                y = f(x0)
                x1 = x0 - y/yprime
                if abs(x1-x0) < 1e-5
                    return x1
                end
                x0 = x1
            end
            error("Max iteration exceeded")
        end
        return [newtonsMethod(.001),newtonsMethod(m/p[1])]
    end

    # adjust bounds
    function adjust(lb,ub)
        x1 = (lb+ub)/2
        x2 = B(x1)
        return x1^(t[1])*x2^(t[2])
    end

    bounds = findIntersection(u)

    # begin recursion
    while true
        if abs(bounds[2]-bounds[1]) > .0001
            u = adjust(bounds[1],bounds[2])
        else
            break
        end
        bounds = findIntersection(u)
    end
    return (bounds[1],I(u,bounds[1]))
end

@time marshallianDemand(100,[3 2],[.3 .7])

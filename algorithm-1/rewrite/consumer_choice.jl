# rewrite in Julia because it is faster than Python and easier than Go

function marshallianDemand(m::Number)

    # define indifference
    function I(utl::Number,x1::Number)
        (utl*x1^(-.3))^(1/.7)
    end

    # define affordability
    function B(x1::Number)
        (m-x1*3)/2
    end

    # set initial affordable guess
    u = (.5*(m/3))^(.3)*(.5*(m/2))^(.7)

    function findIntersection(utl::Float64)
        function f(x1::Float64)
            I(utl,x1) - B(x1)
        end

        # derive using the limit definition
        function derive(x1::Float64)
            h = .00001
            return (f(x1+h)-f(x1))/h
        end

        function newtonsMethod(x0::Float64,maxiter::Integer=50)
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
        return [newtonsMethod(.0001),newtonsMethod(m/3)]
    end

    # adjust bounds
    function adjust(lb,ub)
        x1 = (lb+ub)/2
        x2 = B(x1)
        return x1^(.3)*x2^(.7)
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

@time marshallianDemand(100)
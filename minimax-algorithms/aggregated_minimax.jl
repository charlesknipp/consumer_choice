using Plots
using Printf

# define the comparative statics of the probem in this statement
begin
    m = 10
    p = [1,1]
end

# define the guessed aggregation using a random number generator given the obt-
# ained optimal m_-i from a dynamic program type beat

x_i = (m/p)*rand(Float64)

L() = u(xi) + λ*(p*x')

function isSupermodular()
    # condition for both x_-i and x_i
end

function minimax()
end

function maxmin()
end

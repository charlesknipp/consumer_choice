using Plots

# define some c ∈ C as a vector of goods
c = Array{Float64}
α = Array{Float64}

# define a composite object to help with aggregation on a hyperplane for when we
# eventually consider the case of projective concavity
struct Composite(i)
    x = c[i]
    y = c[1:end.!=i,:]
end

# just use Cobb-Douglas because it is supermodular in c on C = {c|c∈Rⁿ,α≥0}
utility(c,α) = reduce(*,c.^α)
lagrange(c,λ) = utility(c,α) + λ*(m-reduce(+,p.*c))

# the lagrangian is in terms of a vector, should probably rethink how my data is
# structured
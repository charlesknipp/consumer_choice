# Consumer Choice Optimization
An algorithm detailing consumer choice optimization written in Python 3. Since markdown doesn't support `LaTeX` I'm using code blocks to represent inline math

## Notes on the Quasiconvex Approach (two goods)

The construction of the problem is nothing new, however the process of calculating the optimal solution uses an iterative approach that heavily exploits the convex nature of the indifference class. Briefly, the process is as follows:

1. Select a value for `x_1`
 along the indifference curve to create an ordered pair of goods.
2. Convert this selection into set of affordable combinations by determining a budget from `(x_1,x_2)`
.
3. Calculate an upper and lower bound `(\bar x_1, \underline x_1)` along the budget set such that if you were to consume an additional/reduced unit of `x_1` you would be worse off by doing so (respectively).
4. Define a bundle `(x_1,x_2)` that lies in between the previously determined boundary conditions.
5. Repeat this process until the upper and lower bounds are indistinguishable.
6. Return this bundle.

## Notes on the Lagrange Dual Approach (n goods)

Let `f(x)` be the objective constrained by both a sequence of inequalities `g_i(x)` and sequence of equlaity constraints `h_j(x)` respectively indexed by `i \in {1,...,m}` and `j \in {1,...,l}`

Kuhn Tucker States that the following conditions must hold:
1. `g_i(x^*) \geq 0` and `h_j(x^*) = 0`
2. `\mu_i \geq 0`
3. `\mu_i g_i(x*) = 0`
4. `Df_x(x^*) + \sum_{j=1}^{l} \lambda_j^* Dh_j(x^*) + \sum_{i=1}^{m} \mu_i^* Dg_i(x^*) = 0`

## Notes on the n-dimensional Marshallian Approach

This set up mirrors the one in `consumer_choice.py` fairly closely with some minor differences in the definitions of the budget set and utiltiy set to fit higher dimension optimization. The code performs the algorithm of the first one by fixing higher dimensions, and solves for the optimal solution in 2 dimensions; this iteration progresses until increases in the higher dimensions result in lower utility than previous iterations.

I'm still trying to find a better use of convexity in higher dimensions to reduce the time complexity of the algorithm, but it's well on its way.
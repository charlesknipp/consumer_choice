import math
import time


def budget(x,m,p):
    if len(p) != len(x):
        raise IndexError('dim(x) not equal to dim(p)')

    items = [p[i]*x[i] for i in range(len(x))]
    return sum(items)

def cobbDouglas(x,u,t):
    if len(t) != len(x):
        raise IndexError('dim(x) not equal to dim(t)')

    items = [x[i]**t[i] for i in range(len(x))]
    return math.prod(items)

# let $f(x)$ be the objective constrained by both a sequesnce of inequalities
# $g_i(x)$ and sequence of equlaity constraints $h_j(x)$ respectively indexed
# at $i \in {1,...,m}$ and $j \in {1,...,l}$
#
# Kuhn Tucker States that the following conditions must hold.
#   1) $g_i(x^*) \geq 0$ and $h_j(x^*) = 0$
#   2) $\mu_i \geq 0$
#   3) $\mu_i \cdot g_i(x*) = 0$
#   4) $Df_x(x^*) + \sum{j=1}^{l} \lambda_j^* \cdot Dh_j(x^*) + \sum{i=1}^{m} \mu_i^* \cdot Dg_i(x^*) = 0$
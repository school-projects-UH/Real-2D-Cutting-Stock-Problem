from cvxopt import matrix, solvers, glpk
import math

def solve_LP(bins, sheets_per_pattern, sheets):
    w = [b.free_area for b in bins]
    d = [s.demand for s in sheets]
    a = [s.width * s.height for s in sheets]
    m, n = len(w), len(d)
    p = [[0 for _ in range(n)] for _ in range(m)]
    for (j, i), sheets in sheets_per_pattern.items():
        p[j][i] = sheets

    c = matrix([float(wj + sum([p[j][i]*ai for i, ai in enumerate(a)])) for j, wj in enumerate(w)])
    A = matrix([[float(-p[j][i]) for i in range(n)] + [k==j and -1 or 0 for k in range(m)] for j in range(m)])
    b = matrix([float(-di) for di in d] + [0 for i in range(m)])

    # Prevent GLPK from outputing info (comment these lines to see GLPK's output info)
    solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}  # cvxopt 1.1.8
    solvers.options['msg_lev'] = 'GLP_MSG_OFF'  # cvxopt 1.1.7
    solvers.options['LPX_K_MSGLEV'] = 0  # previous versions

    # (_, x) = glpk.ilp(c, A, b, I={i for i in range(len(c))})
    sol = solvers.lp(c, A, b, solver='glpk')
    # fitness = sol['primal objective'] - sum([d[i]*a[i] for i in range(n)])
    x = {f"x{i}":math.ceil(x) for i,x in enumerate(sol['x'])}
    fitness = sum([c[i] * x[f'x{i}'] for i in range(len(x.keys()))]) - sum([d[i]*a[i] for i in range(n)])
    return fitness, x

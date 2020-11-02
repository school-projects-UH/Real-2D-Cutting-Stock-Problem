from cvxopt import matrix, solvers

def solve_LP(bins, sheets_per_pattern, sheets):
    w = [b.free_area for b in bins]
    d = [s.demand for s in sheets]
    a = [s.width * s.height for s in sheets]
    m, n = len(w), len(d)
    p = [[0 for _ in range(n)] for _ in range(m)]
    for (j, i), sheets in sheets_per_pattern.items():
        p[j][i] = sheets

    c = matrix([float(wj + sum([p[j][i]*ai for i, ai in enumerate(a)])) for j, wj in enumerate(w)])
    A = matrix([[float(-p[j][i]) for i in range(n)] for j in range(m)])
    b = matrix([float(-di) for di in d])

    sol = solvers.lp(c, A, b, solver='glpk')
    fitness = sol['primal objective'] 
    fitness = fitness and fitness - sum([d[i]*a[i] for i in range(n)]) or 0

    return fitness, list(sol['x'])
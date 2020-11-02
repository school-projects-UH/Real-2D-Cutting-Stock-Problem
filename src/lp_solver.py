from cvxopt import matrix, solvers, glpk

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

    (_, x) = glpk.ilp(c, A, b, I={i for i in range(len(c))})
    fitness = sum([c[i] * x[i] for i in range(len(x))]) - sum([d[i]*a[i] for i in range(n)])
    x = {f"x{i}":x[i] for i in range(len(x))}
    return fitness, x

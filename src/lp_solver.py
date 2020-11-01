from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD

def solve_LP(bins, sheets_per_pattern, sheets):
    '''
    min * sum(xj* rj) 0 <= j < m
    s.a
    sum(pji * xj) >= di
    xj >= 0
    xj Integer
    '''
    waste = [b.free_area for b in bins]
    demands = [s.demand for s in sheets]
    areas = [s.width * s.height for s in sheets]
    m, n = len(waste), len(demands)
    model = LpProblem(name="cuts", sense=LpMinimize)

    x = { j: LpVariable(f'x{j}', lowBound=0, cat="Integer") for j in range(m)}

    p = [[0 for _ in range(n)] for _ in range(m)]
    for (j, i), sheets in sheets_per_pattern.items():
        p[j][i] = sheets

    def overProduction(j):
        return lpSum(p[i][j] * x[i] * areas[j] for i in range(m)) - demands[j] * areas[j]

    def total_overProduction():
        return lpSum(overProduction(j) for j in range(n))

    for i, di in enumerate(demands):
        model += (lpSum(pj[i] * x[j] for j, pj in enumerate(p)) >= di, f'constrain-{i}')

    model += lpSum([lpSum(x[j] * waste[j] for j in range(m)), total_overProduction()])

    # Solve the optimization problem
    model.solve(solver=PULP_CBC_CMD(msg=0))

    fitness = model.objective.value()
    if fitness == None:
        fitness = 0
    return fitness, {variable.name: variable.varValue for variable in model.variables()}

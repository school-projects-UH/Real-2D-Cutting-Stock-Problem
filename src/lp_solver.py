from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD

def solve_LP(waste, sheets_per_pattern, demands):
    '''
    min * sum(xj* rj) 0 <= j < m
    s.a
    sum(pji * xj) >= di
    xj >= 0
    xj Integer
    '''

    m, n = len(waste), len(demands)
    model = LpProblem(name="cuts", sense=LpMinimize)

    x = { j: LpVariable(f'x{j}', lowBound=0, cat="Integer") for j in range(m)}

    p = [[0 for _ in range(n)] for _ in range(m)]
    for (j, i), sheets in sheets_per_pattern.items():
        p[j][i] = sheets

    for i, di in enumerate(demands):
        model += (lpSum(pj[i] * x[j] for j, pj in enumerate(p)) >= di, f'constrain-{i}')

    model += lpSum(x[j] * waste[j] for j in range(m))

    # Solve the optimization problem
    model.solve(solver=PULP_CBC_CMD(msg=0))

    return model.objective.value(), {variable.name: variable.varValue for variable in model.variables()}

waste = [1, 3]
demands = [10, 15, 13]
sheets_per_pattern = {
    (0, 0): 0, (0, 1): 2, (0, 2): 1, (1, 0): 1, (1, 1): 2, (1, 2): 1
}

print(solve_LP(waste, sheets_per_pattern, demands))
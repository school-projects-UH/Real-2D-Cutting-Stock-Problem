from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable

def solve_LP(r, p, d):
    '''
    min * sum(xj* rj) 0 <= j < m
    s.a
    sum(pji * xj) >= di
    xj >= 0
    xj Integer
    '''

    m = len(r)
    model = LpProblem(name="cuts", sense=LpMinimize)

    x = { j: LpVariable(f'x{j}', lowBound=0, cat="Integer") for j in range(m)}

    for i, di in enumerate(d):
        model += (lpSum(pj[i] * x[j] for j, pj in enumerate(p)) >= di, f'constrain-{i}')

    model += lpSum(x[j] * r[j] for j in range(m))

    # Solve the optimization problem
    status = model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    for var in x.values():
        print(f"{var.name}: {var.value()}")

    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")
    
    return model
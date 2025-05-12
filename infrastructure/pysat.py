from pysat.solvers import Glucose3

def solve_cnf_with_pysat(clauses):
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return model  # Danh sách biến nguyên dương (True) và âm (False)
    else:
        return None

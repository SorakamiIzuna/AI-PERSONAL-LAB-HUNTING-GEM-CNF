from pysat.solvers import Glucose3

def solve_cnf_with_pysat(clauses):
    with Glucose3() as solver:
        for clause in clauses:
            solver.add_clause(clause)
        sat = solver.solve()
        print(sat)
        if sat:
            return solver.get_model()
        else:
            return None



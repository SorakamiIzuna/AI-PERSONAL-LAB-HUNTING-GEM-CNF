def backtracking_solve_cnf(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    sorted_variables = sorted(list(variables))
    assignment = {var_id: None for var_id in sorted_variables}
    if not clauses:
        print(True) 
        return []
    if any(not clause for clause in clauses):
        print(False)
        return None
    solution_assignment = _solve_recursive(clauses, assignment, sorted_variables)
    
    if solution_assignment is not None:
        print(True)
        # Chuyển đổi từ điển `solution_assignment` thành định dạng mô hình
        pysat_model = []
        for var_id in sorted_variables:
            if solution_assignment[var_id]:
                pysat_model.append(var_id)
            else:
                pysat_model.append(-var_id)
        return pysat_model
    else:
        print(False)
        return None

def _solve_recursive(clauses, assignment, sorted_variables):
    for clause in clauses:
        clause_satisfied = False
        clause_has_unassigned_literal = False
        
        for literal in clause:
            var_id = abs(literal)
            value = assignment[var_id] 
            
            if value is None:
                clause_has_unassigned_literal = True
            elif (literal > 0 and value) or (literal < 0 and not value):
                clause_satisfied = True
                break 
        
        if not clause_satisfied and not clause_has_unassigned_literal:
            return None 
    next_var_to_assign = None
    for var_id in sorted_variables:
        if assignment[var_id] is None:
            next_var_to_assign = var_id
            break
    if next_var_to_assign is None:
        return assignment.copy() 

    assignment[next_var_to_assign] = True
    result = _solve_recursive(clauses, assignment, sorted_variables)
    if result is not None:
        return result 

    assignment[next_var_to_assign] = False
    result = _solve_recursive(clauses, assignment, sorted_variables)
    if result is not None:
        return result 
    assignment[next_var_to_assign] = None 
    return None
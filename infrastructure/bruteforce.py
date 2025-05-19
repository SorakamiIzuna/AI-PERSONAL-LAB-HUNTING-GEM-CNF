from domain.cnf_generator import var_id
from itertools import product
def solve_cnf_bruteforce(clauses, grid):
    num_rows, num_cols = len(grid), len(grid[0])
    fixed_assignment = {}
    unfixed_variables = []
    all_possible_vars = set()
    for r in range(num_rows):
        for c in range(num_cols):
            all_possible_vars.add(var_id(r, c, 'T', num_rows, num_cols))
            all_possible_vars.add(var_id(r, c, 'G', num_rows, num_cols))
            all_possible_vars.add(var_id(r, c, 'N', num_rows, num_cols))
    for r in range(num_rows):
        for c in range(num_cols):
            val = grid[r][c]
            vt = var_id(r, c, 'T', num_rows, num_cols)
            vg = var_id(r, c, 'G', num_rows, num_cols)
            vn = var_id(r, c, 'N', num_rows, num_cols)

            if isinstance(val, int):
                fixed_assignment[vn] = True
                fixed_assignment[vt] = False
                fixed_assignment[vg] = False
            else:
                # Ô ẩn: N=False
                fixed_assignment[vn] = False
                # T và G là các biến không cố định cần vét cạn
                unfixed_variables.append(vt)
                unfixed_variables.append(vg)
                
    # Sắp xếp biến không cố định
    unfixed_variables.sort()

    num_unfixed_vars = len(unfixed_variables)
    print(f"\n🔍 Tổng số biến logic: {num_rows * num_cols * 3}")
    print(f"🔒 Số biến cố định (đã biết giá trị): {len(fixed_assignment)}")
    print(f"❓ Số biến cần vét cạn (chưa biết giá trị): {num_unfixed_vars}")
    print(f"🔄 Số lần lặp vét cạn tối đa: 2^{num_unfixed_vars} = {2**num_unfixed_vars}")
    if any(not clause for clause in clauses):
        print(False)
        return None
    if num_unfixed_vars == 0:
        all_satisfied = True
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in fixed_assignment:
                     if (lit > 0 and fixed_assignment[var]) or \
                        (lit < 0 and not fixed_assignment[var]):
                         clause_satisfied = True
                         break
                else:
                     all_satisfied = False
                     break
            if not clause_satisfied:
                all_satisfied = False
                break

        if all_satisfied:
            print(True)
            model_vars = sorted(fixed_assignment.keys())
            model = [var if fixed_assignment[var] else -var for var in model_vars]
            return model
        else:
            print(False)
            return None

    for bits in product([False, True], repeat=num_unfixed_vars):
        unfixed_assignment = {unfixed_variables[i]: bits[i] for i in range(num_unfixed_vars)}
        full_assignment = {**fixed_assignment, **unfixed_assignment}
        all_satisfied = True
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                if (lit > 0 and full_assignment[var]) or \
                   (lit < 0 and not full_assignment[var]):
                    clause_satisfied = True
                    break
            
            if not clause_satisfied:
                all_satisfied = False
                break
        
        if all_satisfied:
            print(True)
            model_vars = sorted(full_assignment.keys())
            model = [var if full_assignment[var] else -var for var in model_vars]
            return model

    print(False)
    return None
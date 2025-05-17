def solve_cnf_bruteforce(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    
    sorted_variables = sorted(list(variables))
    num_vars = len(sorted_variables)

    if num_vars == 0:
        if any(not clause for clause in clauses):
            print(False) 
            return None
        else: 
            print(True)
            return [] 
    for i in range(1 << num_vars):
        current_assignment = {}
        for j in range(num_vars):
            var_value = bool((i >> j) & 1)
            var_id = sorted_variables[j]
            current_assignment[var_id] = var_value
        
        is_satisfying_assignment = True
        for clause in clauses:
            clause_satisfied = False
            for literal in clause:
                var_id = abs(literal)
                var_value = current_assignment[var_id]

                if literal > 0: # Literal dương
                    if var_value: # Nếu biến đó là True
                        clause_satisfied = True
                        break 
                else: # Literal âm
                    if not var_value: # Nếu biến đó là False
                        clause_satisfied = True
                        break 
            
            # Nếu một mệnh đề không được thỏa mãn, cấu hình này không phải là giải pháp
            if not clause_satisfied:
                is_satisfying_assignment = False
                break 
        
        # 4. Nếu tất cả các mệnh đề đều được thỏa mãn, trả về mô hình
        if is_satisfying_assignment:
            print(True)
            # Chuyển đổi cấu hình thành định dạng mô hình mong muốn
            model = []
            for var_id in sorted_variables: # Duyệt theo thứ tự biến đã sắp xếp
                if current_assignment[var_id]:
                    model.append(var_id)
                else:
                    model.append(-var_id)
            # sort() là hàm built-in của list, key=abs cũng là built-in
            model.sort(key=abs) 
            return model
    
    # 5. Nếu không có cấu hình nào thỏa mãn tất cả các mệnh đề
    print(False)
    return None
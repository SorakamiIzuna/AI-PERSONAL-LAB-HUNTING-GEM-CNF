import itertools

def solve_cnf_bruteforce(clauses):
    """
    Giải bài toán CNF bằng phương pháp vét cạn (brute-force).

    Args:
        clauses: Một danh sách các mệnh đề (clauses). Mỗi mệnh đề là một danh sách các literals.
                 Một literal dương (ví dụ: 1) đại diện cho biến đó là True.
                 Một literal âm (ví dụ: -2) đại diện cho biến đó là False.

    Returns:
        Một mô hình (danh sách các literals) nếu CNF có thể thỏa mãn,
        trong đó các số dương biểu thị biến đó là True, số âm biểu thị biến đó là False.
        None nếu CNF không thể thỏa mãn.
    """
    # 1. Xác định tất cả các biến duy nhất có trong các mệnh đề
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    
    # Sắp xếp các biến để đảm bảo thứ tự nhất quán khi gán giá trị
    sorted_variables = sorted(list(variables))
    num_vars = len(sorted_variables)

    # Xử lý trường hợp không có biến hoặc mệnh đề rỗng
    if num_vars == 0:
        # Nếu có bất kỳ mệnh đề rỗng nào (ví dụ: [[]]), CNF không thỏa mãn
        if any(not clause for clause in clauses):
            print(False) # Tương tự print(sat) của pysat
            return None
        else: # Nếu không có biến và không có mệnh đề rỗng (ví dụ: clauses = []), CNF thỏa mãn
            print(True) # Tương tự print(sat) của pysat
            return [] # Trả về mô hình rỗng
            
    # 2. Tạo tất cả các cấu hình giá trị đúng/sai có thể cho các biến
    # itertools.product tạo ra tất cả các kết hợp (True/False) cho số lượng biến
    for assignment_values in itertools.product([True, False], repeat=num_vars):
        # Ánh xạ ID biến với giá trị boolean của nó trong cấu hình hiện tại
        current_assignment = {}
        for i, var_id in enumerate(sorted_variables):
            current_assignment[var_id] = assignment_values[i]
        
        # 3. Kiểm tra xem cấu hình này có thỏa mãn tất cả các mệnh đề hay không
        is_satisfying_assignment = True
        for clause in clauses:
            clause_satisfied = False
            for literal in clause:
                var_id = abs(literal)
                var_value = current_assignment[var_id]

                if literal > 0: # Literal dương (ví dụ: 1)
                    if var_value: # Nếu biến đó là True
                        clause_satisfied = True
                        break # Mệnh đề đã thỏa mãn, chuyển sang mệnh đề tiếp theo
                else: # Literal âm (ví dụ: -2)
                    if not var_value: # Nếu biến đó là False
                        clause_satisfied = True
                        break # Mệnh đề đã thỏa mãn, chuyển sang mệnh đề tiếp theo
            
            # Nếu một mệnh đề không được thỏa mãn, cấu hình này không phải là giải pháp
            if not clause_satisfied:
                is_satisfying_assignment = False
                break # Chuyển sang cấu hình tiếp theo
        
        # 4. Nếu tất cả các mệnh đề đều được thỏa mãn, trả về mô hình
        if is_satisfying_assignment:
            print(True) # Tương tự print(sat) của pysat
            # Chuyển đổi cấu hình thành định dạng mô hình của PySAT (danh sách các literals)
            model = []
            for var_id, value in current_assignment.items():
                if value:
                    model.append(var_id)
                else:
                    model.append(-var_id)
            # Sắp xếp mô hình để nhất quán với đầu ra của PySAT
            model.sort(key=abs) 
            return model
    
    # 5. Nếu không có cấu hình nào thỏa mãn tất cả các mệnh đề
    print(False) # Tương tự print(sat) của pysat
    return None
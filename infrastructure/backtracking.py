def backtracking_solve_cnf(clauses):
    """
    Giải bài toán CNF bằng thuật toán backtracking mà không dùng thư viện ngoài.

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
    
    # Sắp xếp các biến để có thứ tự xử lý nhất quán
    sorted_variables = sorted(list(variables))
    
    # Khởi tạo `assignment`: một từ điển lưu trữ giá trị của biến.
    # Giá trị là True/False nếu đã gán, None nếu chưa gán.
    assignment = {var_id: None for var_id in sorted_variables}

    # Xử lý các trường hợp đặc biệt:
    # 1. CNF rỗng (không có mệnh đề nào) luôn thỏa mãn
    if not clauses:
        print(True) 
        return []

    # 2. CNF chứa mệnh đề rỗng (ví dụ: [[]]) thì không bao giờ thỏa mãn
    if any(not clause for clause in clauses):
        print(False)
        return None

    # Gọi hàm đệ quy để giải quyết
    solution_assignment = _solve_recursive_no_lib(clauses, assignment, sorted_variables)
    
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

def _solve_recursive_no_lib(clauses, assignment, sorted_variables):
    """
    Hàm đệ quy chính thực hiện thuật toán backtracking.
    Không dùng thư viện ngoài.
    
    Args:
        clauses: Danh sách các mệnh đề.
        assignment: Từ điển ánh xạ ID biến với giá trị đã gán (True/False) hoặc None (chưa gán).
        sorted_variables: Danh sách các ID biến đã được sắp xếp.
        
    Returns:
        Một bản sao của từ điển `assignment` nếu tìm thấy giải pháp, nếu không thì None.
    """
    
    # 1. Kiểm tra trạng thái hiện tại của các mệnh đề:
    #    a. Có mệnh đề nào đã bị vi phạm (tất cả literals đều sai) không? -> Quay lui (conflict)
    #    b. Tất cả các mệnh đề đã được thỏa mãn chưa? -> Tìm thấy giải pháp
    #    c. Nếu không phải cả hai, thì vẫn còn mệnh đề chưa xác định -> Tiếp tục phân nhánh

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
            # Conflict detected. Backtrack.
            return None 
    
    # 2. Tìm biến tiếp theo chưa được gán để phân nhánh (branch)
    next_var_to_assign = None
    for var_id in sorted_variables:
        if assignment[var_id] is None:
            next_var_to_assign = var_id
            break
    
    # Nếu không còn biến nào chưa được gán và không có conflict -> đã tìm thấy giải pháp
    if next_var_to_assign is None:
        return assignment.copy() 

    # 3. Phân nhánh: Thử gán `True` cho biến tiếp theo
    assignment[next_var_to_assign] = True
    result = _solve_recursive_no_lib(clauses, assignment, sorted_variables)
    if result is not None:
        return result 

    # 4. Phân nhánh: Nếu gán `True` không dẫn đến giải pháp, thử gán `False`
    assignment[next_var_to_assign] = False
    result = _solve_recursive_no_lib(clauses, assignment, sorted_variables)
    if result is not None:
        return result 

    # 5. Quay lui: Nếu cả hai nhánh đều không dẫn đến giải pháp
    assignment[next_var_to_assign] = None 
    return None
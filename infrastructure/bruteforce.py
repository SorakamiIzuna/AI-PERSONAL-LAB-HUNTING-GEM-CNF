from domain.cnf_generator import var_id
from itertools import product
def solve_cnf_bruteforce(clauses, grid):
    num_rows, num_cols = len(grid), len(grid[0])
    
    # Bước 1: Xác định các biến cố định và giá trị của chúng
    fixed_assignment = {}
    unfixed_variables = []

    # Lấy tất cả các biến có thể có trong công thức
    all_possible_vars = set()
    for r in range(num_rows):
        for c in range(num_cols):
            all_possible_vars.add(var_id(r, c, 'T', num_rows, num_cols))
            all_possible_vars.add(var_id(r, c, 'G', num_rows, num_cols))
            all_possible_vars.add(var_id(r, c, 'N', num_rows, num_cols))
            
    # Xác định biến cố định dựa trên lưới
    for r in range(num_rows):
        for c in range(num_cols):
            val = grid[r][c]
            vt = var_id(r, c, 'T', num_rows, num_cols)
            vg = var_id(r, c, 'G', num_rows, num_cols)
            vn = var_id(r, c, 'N', num_rows, num_cols)

            if isinstance(val, int):
                # Ô số: N=True, T=False, G=False
                fixed_assignment[vn] = True
                fixed_assignment[vt] = False
                fixed_assignment[vg] = False
            else:
                # Ô ẩn: N=False
                fixed_assignment[vn] = False
                # T và G là các biến không cố định cần vét cạn
                unfixed_variables.append(vt)
                unfixed_variables.append(vg)
                
    # Sắp xếp biến không cố định để đầu ra nhất quán (tùy chọn)
    unfixed_variables.sort()

    num_unfixed_vars = len(unfixed_variables)
    print(f"\n🔍 Tổng số biến logic: {num_rows * num_cols * 3}")
    print(f"🔒 Số biến cố định (đã biết giá trị): {len(fixed_assignment)}")
    print(f"❓ Số biến cần vét cạn (chưa biết giá trị): {num_unfixed_vars}")
    print(f"🔄 Số lần lặp vét cạn tối đa: 2^{num_unfixed_vars} = {2**num_unfixed_vars}")

    # Kiểm tra các mệnh đề rỗng ban đầu (không thỏa mãn)
    if any(not clause for clause in clauses):
        print(False)
        return None

    # Xử lý trường hợp không có biến nào cần vét cạn (tất cả đều cố định)
    if num_unfixed_vars == 0:
         # Nếu không có biến nào cần vét cạn, chỉ cần kiểm tra xem gán giá trị cố định có thỏa mãn công thức không
        all_satisfied = True
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                # Lấy giá trị từ fixed_assignment (đã bao gồm tất cả biến cố định)
                if var in fixed_assignment:
                     if (lit > 0 and fixed_assignment[var]) or \
                        (lit < 0 and not fixed_assignment[var]):
                         clause_satisfied = True
                         break
                else:
                     # Trường hợp này không nên xảy ra nếu tất cả biến đều cố định,
                     # nhưng kiểm tra để an toàn.
                     all_satisfied = False
                     break # Thoát khỏi vòng lặp literal
            if not clause_satisfied:
                all_satisfied = False
                break # Thoát khỏi vòng lặp clause

        if all_satisfied:
            print(True)
            # Trả về mô hình từ gán giá trị cố định
            # Lấy tất cả các biến đã được gán giá trị (bao gồm cả cố định)
            model_vars = sorted(fixed_assignment.keys())
            model = [var if fixed_assignment[var] else -var for var in model_vars]
            return model
        else:
            print(False)
            return None


    # Bước 2 & 3: Vét cạn trên các biến không cố định và kết hợp gán giá trị
    for bits in product([False, True], repeat=num_unfixed_vars):
        # Tạo gán giá trị cho các biến không cố định từ bits
        unfixed_assignment = {unfixed_variables[i]: bits[i] for i in range(num_unfixed_vars)}
        
        # Kết hợp gán giá trị cố định và không cố định để có gán giá trị đầy đủ
        full_assignment = {**fixed_assignment, **unfixed_assignment}

        # Bước 4: Kiểm tra công thức với gán giá trị đầy đủ
        all_satisfied = True
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                # Lấy giá trị từ full_assignment
                if (lit > 0 and full_assignment[var]) or \
                   (lit < 0 and not full_assignment[var]):
                    clause_satisfied = True
                    break # Thoát sớm nếu một literal thỏa mãn mệnh đề
            
            if not clause_satisfied:
                all_satisfied = False
                break # Thoát sớm nếu một mệnh đề không được thỏa mãn
        
        if all_satisfied:
            print(True)
            # Xây dựng mô hình từ gán giá trị đầy đủ
            # Lấy tất cả các biến xuất hiện trong full_assignment và sắp xếp chúng
            model_vars = sorted(full_assignment.keys())
            model = [var if full_assignment[var] else -var for var in model_vars]
            return model

    print(False) # Không tìm thấy gán giá trị nào thỏa mãn
    return None
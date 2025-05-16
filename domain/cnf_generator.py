from itertools import combinations

def var_id(row, col, state, num_rows, num_cols):
    base = (row * num_cols + col) * 3
    if state == 'T':
        return base + 1
    elif state == 'G':
        return base + 2
    elif state == 'N':
        return base + 3
    else:
        raise ValueError("state phải là 'T', 'G' hoặc 'N'")

def get_neighbors(row, col, num_rows, num_cols):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                neighbors.append((nr, nc))
    return neighbors


def exactly_k(variables, k):
    clauses = []
    n = len(variables)
    for comb in combinations(variables, k + 1):
        clauses.append([-v for v in comb])
    for comb in combinations(variables, n - k + 1):
        clauses.append([v for v in comb])
    
    return clauses

def generate_cnf(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    clauses = []

    print("🔧 Đang tạo CNF...")
    for row in range(num_rows):
        for col in range(num_cols):
            val = grid[row][col]
            if isinstance(val, int):
                neighbors = get_neighbors(row, col, num_rows, num_cols)
                neighbor_vars = [var_id(r, c, 'T', num_rows, num_cols) for r, c in neighbors]
                print(f"🔢 Ô ({row},{col}) = {val}, có {len(neighbors)} hàng xóm -> ràng buộc bẫy: {neighbor_vars}")
                clauses += exactly_k(neighbor_vars, val)

    for row in range(num_rows):
        for col in range(num_cols):
            val = grid[row][col]
            vt = var_id(row, col, 'T', num_rows, num_cols)
            vg = var_id(row, col, 'G', num_rows, num_cols)
            vn = var_id(row, col, 'N', num_rows, num_cols)

            if isinstance(val, int):
                # This cell contains a number, so its state MUST be 'N' (Number).
                # Clauses to ensure it is *exactly one* of T, G, N:
                clauses.append([vt, vg, vn])
                clauses.append([-vt, -vg])
                clauses.append([-vt, -vn])
                clauses.append([-vg, -vn])
                # CRITICAL ADDITION: Force this cell's state to be 'N'.
                clauses.append([vn])
                print(f"🔒 Ô ({row},{col}) là số: {val} → Ràng buộc: phải là loại N ({vn}). Sẽ không phải T ({-vt}) và không phải G ({-vg}).")
            else:
                clauses.append([-vn])
                clauses.append([vt, vg])
                clauses.append([-vt, -vg])
                print(f"❓ Ô ({row},{col}) là ẩn → chỉ chọn 1 trong T({vt}) hoặc G({vg})")

    return clauses

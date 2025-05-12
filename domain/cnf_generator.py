from itertools import combinations

# Hàm ánh xạ tọa độ (i, j) thành biến CNF số nguyên
def var_id(row, col, num_cols):
    return row * num_cols + col + 1

# Hàm lấy 8 vị trí lân cận (trong giới hạn lưới)
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

# Sinh CNF dạng exactly-k (chính xác k biến là True) trong số N biến
def exactly_k(variables, k):
    clauses = []

    # Ít nhất k biến: chọn mọi tổ hợp (k) và OR lại
    if len(variables) >= k:
        at_least_k = [list(comb) for comb in combinations(variables, k)]
        clauses += [list(clause) for clause in at_least_k]

    # Không quá k biến: với mọi tổ hợp (k+1), ít nhất 1 phải là False
    for comb in combinations(variables, k + 1):
        clauses.append([-v for v in comb])

    return clauses

# Hàm chính sinh CNF từ grid
def generate_cnf(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    clauses = []

    for row in range(num_rows):
        for col in range(num_cols):
            cell_value = grid[row][col]
            if isinstance(cell_value, int):  # Chỉ xử lý ô có số
                neighbors = get_neighbors(row, col, num_rows, num_cols)
                neighbor_vars = [var_id(r, c, num_cols) for r, c in neighbors]
                clauses += exactly_k(neighbor_vars, cell_value)

    return clauses

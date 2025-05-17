from infrastructure.file_loader import load_grid_from_file
from domain.cnf_generator import generate_cnf
from infrastructure.pysat import solve_cnf_with_pysat
from infrastructure.bruteforce import solve_cnf_bruteforce
from infrastructure.backtracking import backtracking_solve_cnf
from domain.cnf_generator import var_id
def decode_model(model, grid):
    num_rows, num_cols = len(grid), len(grid[0])
    board = [["?" for _ in range(num_cols)] for _ in range(num_rows)]

    print("\n🔍 Đang giải mã lời giải:")
    for row in range(num_rows):
        for col in range(num_cols):
            v_t = var_id(row, col, 'T', num_rows, num_cols)
            v_g = var_id(row, col, 'G', num_rows, num_cols)
            v_n = var_id(row, col, 'N', num_rows, num_cols)

            if v_n in model:
                board[row][col] = str(grid[row][col])
                print(f"  N Ô ({row},{col}) → số: {board[row][col]}")
            elif v_t in model:
                board[row][col] = "T"
                print(f"  T Ô ({row},{col}) → Bẫy")
            elif v_g in model:
                board[row][col] = "G"
                print(f"  G Ô ({row},{col}) → Gem")
            else:
                board[row][col] = "?"
                print(f"  ❓ Ô ({row},{col}) → Không rõ")

    return board
def run_game():
    print("🔄 Đang đọc bản đồ từ file...")
    grid = load_grid_from_file("./data/input_5x5.txt")

    print("\n📦 Bản đồ gốc:")
    for row in grid:
        print(" ".join(str(x) if x is not None else "_" for x in row))

    print("\n🧠 Đang sinh CNF từ bản đồ...")
    clauses = generate_cnf(grid)
    print(f"📄 Số mệnh đề CNF: {len(clauses)}")

    print("PySAT")
    pysat_model = solve_cnf_with_pysat(clauses)

    if pysat_model is None:
        print("❌ Không tìm được lời giải.")
        return

    print("Solved")
    board = decode_model(pysat_model, grid)

    for row in board:
        print(" ".join(row))
    print("Backtracking")

    backtracking_model = backtracking_solve_cnf(clauses)
    if backtracking_model is None:
        print("❌ Không tìm được lời giải.")
        return

    print("Solved")
    board = decode_model(backtracking_model, grid)

    for row in board:
        print(" ".join(row))



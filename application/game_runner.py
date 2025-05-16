from infrastructure.file_loader import load_grid_from_file
from domain.cnf_generator import generate_cnf
from infrastructure.pysat import solve_cnf_with_pysat
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
                print(f"  ✅ Ô ({row},{col}) → số: {board[row][col]}")
            elif v_t in model:
                board[row][col] = "💣"
                print(f"  💣 Ô ({row},{col}) → Bẫy")
            elif v_g in model:
                board[row][col] = "💎"
                print(f"  💎 Ô ({row},{col}) → Gem")
            else:
                board[row][col] = "?"
                print(f"  ❓ Ô ({row},{col}) → Không rõ")

    return board
def run_game():
    print("🔄 Đang đọc bản đồ từ file...")
    grid = load_grid_from_file("./data/input_1.txt")

    print("\n📦 Bản đồ gốc:")
    for row in grid:
        print(" ".join(str(x) if x is not None else "_" for x in row))

    print("\n🧠 Đang sinh CNF từ bản đồ...")
    clauses = generate_cnf(grid)
    print(f"📄 Số mệnh đề CNF: {len(clauses)}")

    print("\n🤖 Đang giải bằng PySAT...")
    model = solve_cnf_with_pysat(clauses)

    if model is None:
        print("❌ Không tìm được lời giải.")
        return

    print("✅ Đã tìm thấy lời giải!")
    num_rows, num_cols = len(grid), len(grid[0])
    board = decode_model(model, grid)


    print("\n🗺️ Bản đồ kết quả:")
    for row in board:
        print(" ".join(row))



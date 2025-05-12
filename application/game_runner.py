from infrastructure.file_loader import load_grid_from_json
from domain.cnf_generator import generate_cnf
from infrastructure.pysat import solve_cnf_with_pysat

def run_game():
    grid = load_grid_from_json("data/level1.json")
    print("📦 Bản đồ đã đọc:")
    for row in grid:
        print(row)

    print("\n🧠 Đang sinh CNF từ bản đồ...")
    clauses = generate_cnf(grid)
    print(f"📄 Số mệnh đề CNF: {len(clauses)}")

    print("\n🤖 Đang giải bằng PySAT...")
    model = solve_cnf_with_pysat(clauses)

    if model is None:
        print("❌ Không tìm được lời giải.")
    else:
        print("✅ Đã tìm thấy lời giải!")
        num_rows, num_cols = len(grid), len(grid[0])
        board = [["?" for _ in range(num_cols)] for _ in range(num_rows)]

        for val in model:
            if val > 0:
                i = (val - 1) // num_cols
                j = (val - 1) % num_cols
                board[i][j] = "💣"  # Trap
            elif val < 0:
                i = (-val - 1) // num_cols
                j = (-val - 1) % num_cols
                board[i][j] = "💎"  # Gem

        print("\n🗺️ Bản đồ kết quả:")
        for row in board:
            print(" ".join(row))


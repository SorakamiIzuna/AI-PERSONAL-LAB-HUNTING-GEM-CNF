from infrastructure.file_loader import load_grid_from_json
from domain.cnf_generator import generate_cnf

def run_game():
    grid = load_grid_from_json("data/level1.json")
    print("📦 Bản đồ đã đọc:")
    for row in grid:
        print(row)

    print("\n🧠 Đang sinh CNF từ bản đồ...")
    clauses = generate_cnf(grid)

    print(f"📄 Số mệnh đề CNF sinh ra: {len(clauses)}")
    print("📜 Một số mệnh đề đầu tiên:")
    for i, clause in enumerate(clauses[:10]):  # In thử 10 mệnh đề đầu
        print(f"{i + 1}: {clause}")


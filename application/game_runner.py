from infrastructure.file_loader import load_grid_from_json

def run_game():
    grid = load_grid_from_json("data/level1.json")
    print("📦 Bản đồ đã đọc:")
    for row in grid:
        print(row)

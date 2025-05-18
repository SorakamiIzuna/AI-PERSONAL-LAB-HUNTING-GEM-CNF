from infrastructure.file_loader import load_grid_from_file
from domain.cnf_generator import generate_cnf
from infrastructure.pysat import solve_cnf_with_pysat
from infrastructure.bruteforce import solve_cnf_bruteforce
from infrastructure.backtracking import backtracking_solve_cnf
from domain.cnf_generator import var_id
import time

filepath = "./testcases/input/input_11x11.txt"
output_filepath = "./testcases/output/output_11x11.txt"

def decode_model(model, grid):
    num_rows, num_cols = len(grid), len(grid[0])
    board = [["?" for _ in range(num_cols)] for _ in range(num_rows)]

    print("\n🔍 Đang giải mã lời giải:")
    output_lines = ["\n🔍 Đang giải mã lời giải:"]
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
    print(" Đang đọc bản đồ từ file...")
    grid = load_grid_from_file(filepath)

    print("\nBản đồ gốc:")
    for row in grid:
        print(" ".join(str(x) if x is not None else "_" for x in row))

    output_content = [""]

    print("\nĐang sinh CNF từ bản đồ...")
    clauses = generate_cnf(grid)
    print(f" Số mệnh đề CNF: {len(clauses)}")

    #--------------------PYSAT--------------------------------
    print("PySAT")
    output_content.append("PySAT")
    start_time = time.time()
    pysat_model = solve_cnf_with_pysat(clauses)
    end_time = time.time()
    pysat_duration = end_time - start_time
    print(f"Thời gian giải bằng PySAT: {pysat_duration:.4f} giây")
    output_content.append(f"Thời gian giải bằng PySAT: {pysat_duration:.4f} giây")

    if pysat_model is None:
        print("Không tìm được lời giải bằng PySAT.")
        output_content.append("Không tìm được lời giải bằng PySAT.")
        pysat_board = [["?" for _ in range(len(grid[0]))] for _ in range(len(grid))]
    else:
        print("Solved by PySAT")
        output_content.append("Solved by PySAT")
        pysat_board= decode_model(pysat_model, grid)

    print("\nLời giải bằng PySAT:")
    output_content.append("\nLời giải bằng PySAT:")
    for row in pysat_board:
        print(" ".join(row))
        output_content.append(" ".join(row))

    #--------------------------BACKTRACKING-------------------
    print("\nBacktracking")
    output_content.append("\nBacktracking")
    start_time = time.time()
    backtracking_model = backtracking_solve_cnf(clauses)
    end_time = time.time()
    backtracking_duration = end_time - start_time
    print(f"Thời gian giải bằng Backtracking: {backtracking_duration:.4f} giây")
    output_content.append(f"Thời gian giải bằng Backtracking: {backtracking_duration:.4f} giây")
    if backtracking_model is None:
        print("Không tìm được lời giải bằng Backtracking.")
        output_content.append("Không tìm được lời giải bằng Backtracking.")
        backtracking_board = [["?" for _ in range(len(grid[0]))] for _ in range(len(grid))]
    else:
        print("Solved by Backtracking")
        output_content.append("Solved by Backtracking")
        backtracking_board = decode_model(backtracking_model, grid)
    print("\nLời giải bằng Backtracking:")
    output_content.append("\nLời giải bằng Backtracking:")
    for row in backtracking_board:
        print(" ".join(row))
        output_content.append(" ".join(row))

    #--------------------------BRUTEFORCE-------------------
    print("\nBruteforce")
    output_content.append("\nBruteforce")
    start_time = time.time()
    bruteforce_model = solve_cnf_bruteforce(clauses, grid)
    end_time = time.time()
    bruteforce_duration = end_time - start_time
    print(f"Thời gian giải bằng Bruteforce: {bruteforce_duration:.4f} giây")
    output_content.append(f"Thời gian giải bằng Bruteforce: {bruteforce_duration:.4f} giây")
    if bruteforce_model is None:
        print("Không tìm được lời giải bằng Bruteforce.")
        output_content.append("Không tìm được lời giải bằng Bruteforce.")
        bruteforce_board = [["?" for _ in range(len(grid[0]))] for _ in range(len(grid))]
    else:
        print("Solved by Bruteforce")
        output_content.append("Solved by Bruteforce")
        bruteforce_board= decode_model(bruteforce_model, grid)

    print("\nLời giải bằng Bruteforce:")
    output_content.append("\nLời giải bằng Bruteforce:")
    for row in bruteforce_board:
        print(" ".join(row))
        output_content.append(" ".join(row))

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(output_content))
    print(f"\n✅ Đã chép kết quả vào file: {output_filepath}")

if __name__ == "__main__":
    run_game()
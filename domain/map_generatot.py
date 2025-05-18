import random

def generate_grid(n, bomb_count, gem_count):
    grid = [['' for _ in range(n)] for _ in range(n)]

    # Đặt bom 'T'
    bomb_positions = set()
    while len(bomb_positions) < bomb_count:
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        bomb_positions.add((i, j))
    for i, j in bomb_positions:
        grid[i][j] = 'T'

    # Đặt gem 'G' (không đè lên bom)
    gem_positions = set()
    while len(gem_positions) < gem_count:
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        if (i, j) not in bomb_positions and grid[i][j] == '':
            grid[i][j] = 'G'
            gem_positions.add((i, j))

    # Tính số cho các ô còn lại
    for i in range(n):
        for j in range(n):
            if grid[i][j] != '':
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] == 'T':
                        count += 1
            grid[i][j] = str(count)

    return grid

def print_grid(grid):
    for row in grid:
        output_row = []
        for cell in row:
            if cell in {'T', 'G'}:
                output_row.append('_,')
            else:
                output_row.append(f"{cell},")
        print("".join(output_row))


# Ví dụ
random.seed(42)  # Tái lập được
map_generated = generate_grid(n=20, bomb_count=60, gem_count=35)
print_grid(map_generated)

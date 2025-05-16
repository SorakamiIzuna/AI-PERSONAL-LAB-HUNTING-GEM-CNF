def load_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # bỏ qua dòng trống
            # Tách theo dấu phẩy, có thể thêm strip cho từng ô
            cells = [c.strip() for c in line.split(',')]
            row = []
            for c in cells:
                if c == '_' or c == '' or c.lower() == 'empty':
                    row.append(None)  # ô chưa biết
                else:
                    try:
                        val = int(c)
                        row.append(val)  # ô số
                    except ValueError:
                        raise ValueError(f"Giá trị không hợp lệ trong file: {c}")
            grid.append(row)
    return grid


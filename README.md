# AI-PERSONAL-LAB
22120010 - Hoàng Tuấn Anh
Các map được đặt trong /testcases/input và kết quả được đặt trong /testcases/output

Để đổi map ta vào /application/game_runner và đổi filepath thành các map tương ứng
Ví dụ:
    filepath = "./testcases/input/input_5x5.txt"
    output_filepath = "./testcases/output/output_5x5.txt"

Sau đó chạy main.py. Chương trình sẽ lần lượt chạy Pysat > Backtracking > Bruteforce và lưu kết quả vào /testcases/output

Có thể tạo các map kích thước khác bằng cách dùng /domain/map_generator.py bằng cách thay các tham số vào
    map_generated = generate_grid(n=7, bomb_count=11, gem_count=3)

    với n: kích thước map, bomb_count: số bom, gem_count: số gem

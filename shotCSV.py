import csv
import matplotlib.pyplot as plt

# CSVファイルのパス
csv_file_path = "./csv/ball_positions.csv"  # ファイルパスを適切に設定

# データを格納するリスト
frame_numbers = []
x_values = []
y_values = []

# CSVファイルを読み込み、データをリストに格納
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        frame_numbers.append(int(row['Frame']))
        x_values.append(int(row['X']))
        y_values.append(int(row['Y']))

# グラフ1: 横軸にフレームナンバー、縦軸にxの値
plt.figure(1)
plt.plot(frame_numbers, x_values, marker='o')
plt.xlabel('Frame Number')
plt.ylabel('X Value')
plt.title('X Value vs Frame Number')

# グラフ2: 横軸にフレームナンバー、縦軸にyの値
plt.figure(2)
plt.plot(frame_numbers, y_values, marker='o', color='green')
plt.xlabel('Frame Number')
plt.ylabel('Y Value')
plt.title('Y Value vs Frame Number')

# グラフを表示
plt.show()

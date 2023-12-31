import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

# Tkinterルートウィンドウの初期化
root = tk.Tk()
root.withdraw()

# ファイル選択ダイアログを表示
csv_file_path = filedialog.askopenfilename(title="CSVファイルを選択してください", filetypes=[("CSV files", "*.csv")])

# ファイルが選択されなかった場合の処理
if not csv_file_path:
    print("ファイルが選択されませんでした。プログラムを終了します。")
    exit()

# ファイル名から拡張子を除いて基本名を取得
base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
print(base_name)
# データを格納するリスト
frame_numbers = []
x_values = []
y_values = []

# CSVファイルを読み込み、データをリストに格納
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    prev_x = None
    prev_y = None
    for row in csv_reader:
        frame_numbers.append(int(row['Frame']))
        # 空の文字列の場合は None を追加
        x = int(row['X']) if row['X'] else None
        y = int(row['Y']) if row['Y'] else None
        # 前のボールの位置と比べて100以上離れていたらそのポイントはNoneとする
        if prev_x is not None and x is not None and abs(prev_x - x) >= 100:
            x = None
        if prev_y is not None and y is not None and abs(prev_y - y) >= 100:
            y = None
        x_values.append(x)
        y_values.append(y)
        prev_x = x if x is not None else None
        prev_y = y if y is not None else None

# 保存先ディレクトリのパス
save_dir = os.path.join('./csv/graph/', base_name)

# ディレクトリが存在しない場合は作成
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 100フレームごとにデータを分割してグラフを生成
for i in range(0, len(frame_numbers), 100):
    # 分割するデータの範囲を設定
    end = i + 100
    if end > len(frame_numbers):
        end = len(frame_numbers)

    # グラフ1: X値
    plt.figure()
    plt.plot(frame_numbers[i:end], x_values[i:end], marker='o')
    plt.xlabel('Frame Number')
    plt.ylabel('X Value')
    plt.title(f'X Value vs Frame Number ({i+1}-{end})')
    x_value_graph_filename = os.path.join(save_dir, f'x_value_{i+1}_{end}.png')
    plt.savefig(x_value_graph_filename)
    plt.close()

    # グラフ2: Y値
    plt.figure()
    plt.plot(frame_numbers[i:end], y_values[i:end], marker='o', color='green')
    plt.xlabel('Frame Number')
    plt.ylabel('Y Value')
    plt.title(f'Y Value vs Frame Number ({i+1}-{end})')
    y_value_graph_filename = os.path.join(save_dir, f'y_value_{i+1}_{end}.png')
    plt.savefig(y_value_graph_filename)
    plt.close()

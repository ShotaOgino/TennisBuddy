import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np

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
    for row in csv_reader:
        frame_numbers.append(int(row['Frame']))
        x_values.append(int(row['X']))
        y_values.append(int(row['Y']))

# 保存先ディレクトリのパス
save_dir = os.path.join('./csv/graph/', base_name)

# ディレクトリが存在しない場合は作成
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# フレーム番号に基づいてデータを分割
frame_bins = np.arange(0, max(frame_numbers) + 101, 100)

# フレーム番号ごとにデータを分割してグラフを生成
for i in range(len(frame_bins) - 1):
    start_frame = frame_bins[i]
    end_frame = frame_bins[i+1] - 1
    idx = np.where((frame_numbers >= start_frame) & (frame_numbers < end_frame))

    # グラフ1: X値
    plt.figure()
    plt.plot(np.array(frame_numbers)[idx], np.array(x_values)[idx], marker='o')
    plt.xlabel('Frame Number')
    plt.ylabel('X Value')
    plt.title(f'X Value vs Frame Number ({start_frame+1}-{end_frame})')
    x_value_graph_filename = os.path.join(save_dir, f'x_value_{start_frame+1}_{end_frame}.png')
    plt.savefig(x_value_graph_filename)
    plt.close()

    # グラフ2: Y値
    plt.figure()
    plt.plot(np.array(frame_numbers)[idx], np.array(y_values)[idx], marker='o', color='green')
    plt.xlabel('Frame Number')
    plt.ylabel('Y Value')
    plt.title(f'Y Value vs Frame Number ({start_frame+1}-{end_frame})')
    y_value_graph_filename = os.path.join(save_dir, f'y_value_{start_frame+1}_{end_frame}.png')
    plt.savefig(y_value_graph_filename)
    plt.close()

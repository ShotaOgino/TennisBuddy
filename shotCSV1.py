import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

# ファイル選択ダイアログを表示
csv_file_path = filedialog.askopenfilename(title="CSVファイルを選択してください", filetypes=[("CSV files", "*.csv")])

# ファイルが選択されなかった場合の処理
if not csv_file_path:
    print("ファイルが選択されませんでした。プログラムを終了します。")
    exit()

# Tkinterのメインループを終了
tk.Tk().quit()

# ファイル名から拡張子を除いて基本名を取得
base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
print(base_name)

frame_numbers = []
y_values = []
bounce_points = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        frame_numbers.append(int(row['Frame']))
        y = int(row['Y']) if row['Y'] else None
        y_values.append(y)

# Y座標の変化率を計算
y_values = np.array(y_values, dtype=float)
change_y = np.diff(y_values)

# 平滑化前のグラフを描画
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(frame_numbers[:-1], change_y, label='Before smoothing')
plt.legend()

# 平滑化
smoothed_change_y = moving_average(change_y, 3)  # ウィンドウサイズは調整可能

# 平滑化後のグラフを描画
plt.subplot(1, 2, 2)
plt.plot(frame_numbers[:-3], smoothed_change_y, label='After smoothing')
plt.legend()

plt.show()

# バウンド検出
for i in range(1, len(smoothed_change_y) - 1):
    if smoothed_change_y[i-1] < 0 and smoothed_change_y[i] > 0 and abs(smoothed_change_y[i]) > 10:  # 閾値は要調整
        frame = frame_numbers[i + 1]  # np.diff により1フレームずれるため
        bounce_points.append(frame)

""" # バウンドポイントの出力
plt.figure()
plt.plot(frame_numbers, y_values)
for frame in bounce_points:
    print(f"Frame: {frame}")
    plt.scatter(frame, y_values[frame_numbers.index(frame)], color='red')  # バウンドポイントを赤色でプロット
plt.show() """

import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
from scipy.optimize import curve_fit

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
        # 空の文字列の場合は None を追加
        x = int(row['X']) if row['X'] else None
        y = int(row['Y']) if row['Y'] else None
        """ # 前のボールの位置と比べて80以上離れていたらそのポイントはNoneとする
        if prev_x is not None and x is not None and abs(prev_x - x) >= 80:
            x = None
        if prev_y is not None and y is not None and abs(prev_y - y) >= 80:
            y = None """
        if y is not None:  # yがNoneでない場合のみframe_numbersとy_valuesに追加
            frame_numbers.append(int(row['Frame']))
            x_values.append(x)
            y_values.append(y)
        prev_x = x if x is not None else None
        prev_y = y if y is not None else None

# Filter out None values from y_values
y_values = [value for value in y_values if value is not None]

# Define a polynomial function to fit
def poly_func(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

# Fit the data to the polynomial function
popt, pcov = curve_fit(poly_func, np.array(frame_numbers), np.array(y_values))

# Generate x values for the fit curve
x_fit = np.linspace(min(frame_numbers), max(frame_numbers), 500)
# Generate y values for the fit curve
y_fit = poly_func(x_fit, *popt)

# Plotting the data and the fit curve
plt.figure(figsize=(12, 6))
plt.scatter(frame_numbers, y_values, label='Data', color='blue')
plt.plot(x_fit, y_fit, label='Approximation Function', color='red')
plt.title('Graph with Approximation Function')
plt.xlabel('Frame')
plt.ylabel('Y Values')
plt.legend()
plt.grid(True)
plt.show()
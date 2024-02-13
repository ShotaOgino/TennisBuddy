import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
from scipy.ndimage import gaussian_filter1d
from numpy.polynomial import Polynomial

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
y_values = []

# CSVファイルを読み込み、データをリストに格納
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        y = int(row['Y']) if row['Y'] else None
        if y is not None:  # yがNoneでない場合のみframe_numbersとy_valuesに追加
            frame_numbers.append(int(row['Frame']))
            y_values.append(y)

# Filter out None values from y_values
y_values = [value for value in y_values if value is not None]

# Create a data chunk
data_chunk = {'Frame': np.array(frame_numbers), 'Y': np.array(y_values)}

def fit_polynomial_with_smoothing(data_chunk, degree=7, smoothing_sigma=2):
    # Apply Gaussian smoothing to the Y values
    smoothed_y = gaussian_filter1d(data_chunk['Y'], sigma=smoothing_sigma)

    # Fit a polynomial of the specified degree to the smoothed data
    x = data_chunk['Frame']
    p = Polynomial.fit(x, smoothed_y, degree).convert()

    # Create a string representation of the polynomial
    coef = p.coef[::-1]  # Reverse to match the standard polynomial format
    terms = [f"{coef[i]:.2f}x^{len(coef)-i-1}" for i in range(len(coef)) if abs(coef[i]) > 1e-2]  # Ignore very small coefficients
    polynomial_formula = " + ".join(terms).replace("x^1", "x").replace("x^0", "").replace("+-", "- ")

    return p, polynomial_formula, smoothed_y

# Fit the polynomial with smoothing
polynomial, formula, smoothed_y = fit_polynomial_with_smoothing(data_chunk)

# Generate values for plotting
frames = np.linspace(data_chunk['Frame'].min(), data_chunk['Frame'].max(), 500)
fitted_values = polynomial(frames)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(data_chunk['Frame'], data_chunk['Y'], color='blue', label='Original Data Points')
plt.plot(data_chunk['Frame'], smoothed_y, color='orange', label='Smoothed Data')
plt.plot(frames, fitted_values, color='red', label='Fitted Polynomial (Degree 7)')
plt.title(f'{formula}')
plt.xlabel('Frame')
plt.ylabel('Y Position')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"./csv/{base_name}.png")  # Add this line
plt.show()

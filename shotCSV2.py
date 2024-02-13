import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
import catboost as ctb
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.spatial import distance

class BounceDetector:
    def __init__(self, path_model=None):
        self.model = ctb.CatBoostRegressor()
        self.threshold = 0.45
        if path_model:
            self.load_model(path_model)
        
    def load_model(self, path_model):
        self.model.load_model(path_model)
    
    def prepare_features(self, x_ball, y_ball):
        labels = pd.DataFrame({'frame': range(len(x_ball)), 'x-coordinate': x_ball, 'y-coordinate': y_ball})
        
        num = 3
        eps = 1e-15
        for i in range(1, num):
            labels['x_lag_{}'.format(i)] = labels['x-coordinate'].shift(i)
            labels['x_lag_inv_{}'.format(i)] = labels['x-coordinate'].shift(-i)
            labels['y_lag_{}'.format(i)] = labels['y-coordinate'].shift(i)
            labels['y_lag_inv_{}'.format(i)] = labels['y-coordinate'].shift(-i) 
            labels['x_diff_{}'.format(i)] = abs(labels['x_lag_{}'.format(i)] - labels['x-coordinate'])
            labels['y_diff_{}'.format(i)] = labels['y_lag_{}'.format(i)] - labels['y-coordinate']
            labels['x_diff_inv_{}'.format(i)] = abs(labels['x_lag_inv_{}'.format(i)] - labels['x-coordinate'])
            labels['y_diff_inv_{}'.format(i)] = labels['y_lag_inv_{}'.format(i)] - labels['y-coordinate']
            labels['x_div_{}'.format(i)] = abs(labels['x_diff_{}'.format(i)]/(labels['x_diff_inv_{}'.format(i)] + eps))
            labels['y_div_{}'.format(i)] = labels['y_diff_{}'.format(i)]/(labels['y_diff_inv_{}'.format(i)] + eps)

        for i in range(1, num):
            labels = labels[labels['x_lag_{}'.format(i)].notna()]
            labels = labels[labels['x_lag_inv_{}'.format(i)].notna()]
        labels = labels[labels['x-coordinate'].notna()] 
        
        colnames_x = ['x_diff_{}'.format(i) for i in range(1, num)] + \
                     ['x_diff_inv_{}'.format(i) for i in range(1, num)] + \
                     ['x_div_{}'.format(i) for i in range(1, num)]
        colnames_y = ['y_diff_{}'.format(i) for i in range(1, num)] + \
                     ['y_diff_inv_{}'.format(i) for i in range(1, num)] + \
                     ['y_div_{}'.format(i) for i in range(1, num)]
        colnames = colnames_x + colnames_y

        features = labels[colnames]
        return features, list(labels['frame'])
    
    def predict(self, x_ball, y_ball, smooth=True):
        if y_ball is not None and not np.isnan(y_ball).any() and not np.isinf(y_ball).any():
            print(f"Before smoothing, y_ball contains non-finite values: {np.isnan(y_ball).any() or np.isinf(y_ball).any()}")
        if smooth:
            x_ball, y_ball = self.smooth_predictions(x_ball, y_ball)
        if y_ball is not None and not np.isnan(y_ball).any() and not np.isinf(y_ball).any():
            print(f"After smoothing, y_ball contains non-finite values: {np.isnan(y_ball).any() or np.isinf(y_ball).any()}")
        features, num_frames = self.prepare_features(x_ball, y_ball)
        preds = self.model.predict(features)
        ind_bounce = np.where(preds > self.threshold)[0]
        if len(ind_bounce) > 0:
            ind_bounce = self.postprocess(ind_bounce, preds)
        frames_bounce = [num_frames[x] for x in ind_bounce]
        return set(frames_bounce)
    
    def smooth_predictions(self, x_ball, y_ball):
        is_none = [int(x is None) for x in x_ball]
        interp = 5
        counter = 0
        for num in range(interp, len(x_ball)-1):
            if not x_ball[num] and sum(is_none[num-interp:num]) == 0 and counter < 3:
                if y_ball[num-interp:num] is not None and not np.isnan(y_ball[num-interp:num]).any() and not np.isinf(y_ball[num-interp:num]).any():
                    print(f"Before extrapolation, y_ball[{num-interp}:{num}] contains non-finite values: {np.isnan(y_ball[num-interp:num]).any() or np.isinf(y_ball[num-interp:num]).any()}")
                x_ext, y_ext = self.extrapolate(x_ball[num-interp:num], y_ball[num-interp:num])
                x_ball[num] = x_ext
                y_ball[num] = y_ext
                is_none[num] = 0
                if x_ball[num+1] is not None and y_ball[num+1] is not None:
                    dist = distance.euclidean((x_ext, y_ext), (x_ball[num+1], y_ball[num+1]))
                    if dist > 80:
                        x_ball[num+1], y_ball[num+1], is_none[num+1] = None, None, 1
                counter += 1
            else:
                counter = 0  
        return x_ball, y_ball

    def extrapolate(self, x_coords, y_coords):
        xs = list(range(len(x_coords)))
        func_x = CubicSpline(xs, x_coords, bc_type='natural')
        x_ext = func_x(len(x_coords))
        func_y = CubicSpline(xs, y_coords, bc_type='natural')
        y_ext = func_y(len(x_coords))
        return float(x_ext), float(y_ext)    

    def postprocess(self, ind_bounce, preds):
        ind_bounce_filtered = [ind_bounce[0]]
        for i in range(1, len(ind_bounce)):
            if (ind_bounce[i] - ind_bounce[i-1]) != 1:
                cur_ind = ind_bounce[i]
                ind_bounce_filtered.append(cur_ind)
            elif preds[ind_bounce[i]] > preds[ind_bounce[i-1]]:
                ind_bounce_filtered[-1] = ind_bounce[i]
        return ind_bounce_filtered

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

# データを格納するリスト
frame_numbers = []
x_values = []
y_values = []
x_values_original = []  # 操作前のx_valuesを保存するためのリストを追加

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
        x_values_original.append(x)  # 操作前のxを保存
        # 前のボールの位置と比べて80以上離れていたらそのポイントはNoneとする
        if prev_x is not None and x is not None and abs(prev_x - x) >= 80:
            x = None
        if prev_y is not None and y is not None and abs(prev_y - y) >= 80:
            y = None
        x_values.append(x)
        y_values.append(y)
        prev_x = x if x is not None else prev_x
        prev_y = y if y is not None else prev_y

# Replace None values with np.nan
x_values_original = [value if value is not None else np.nan for value in x_values_original]  # 操作前のx_valuesもnp.nanで置き換え
x_values = [value if value is not None else np.nan for value in x_values]
y_values = [value if value is not None else np.nan for value in y_values]

# モデルのパスを指定
path_model = "/Users/shota/Coding/TennisBuddy/weights/ctb_regr_bounce.cbm"

# BounceDetectorのインスタンスを作成
detector = BounceDetector(path_model)

# バウンスが発生したフレームを予測
bounce_frames = detector.predict(x_values, y_values)

print(bounce_frames)

# ボールの軌跡をプロット
plt.plot(frame_numbers, x_values_original, label='Original Ball Path')  # 操作前のx_valuesをプロット
plt.plot(frame_numbers, x_values, label='Ball Path')

# バウンスしたフレームのインデックスを取得
bounce_indices = [frame_numbers.index(frame) for frame in bounce_frames]

# バウンスした点をプロット
plt.scatter([frame_numbers[i] for i in bounce_indices], [x_values[i] for i in bounce_indices], color='red', label='Bounce Points')

plt.xlabel('Frame Number')
plt.ylabel('X Value')
plt.legend()
plt.show()
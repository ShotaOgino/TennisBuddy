import catboost as ctb
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import distance
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

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
        if smooth:
            x_ball, y_ball = self.smooth_predictions(x_ball, y_ball)
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
                x_ext, y_ext = self.extrapolate(x_ball[num-interp:num], y_ball[num-interp:num])
                x_ball[num] = x_ext
                y_ball[num] = y_ext
                is_none[num] = 0
                if x_ball[num+1]:
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

# GUIでCSVファイルを選択する関数
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Tkのメインウィンドウを表示しない
    file_path = filedialog.askopenfilename(
        title="CSVファイルを選択してください",
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path

# BounceDetectorクラスのインスタンスを作成
detector = BounceDetector(path_model='/Users/shota/Coding/TennisBuddy/weights/ctb_regr_bounce.cbm')

# CSVファイルをGUIで選択
csv_file_path = select_csv_file()
if csv_file_path:
    data = pd.read_csv(csv_file_path)
    # バウンド地点を推定
    frames_bounce = detector.predict(data['X'], data['Y'])

    # グラフに表示
    plt.figure(figsize=(10, 6))
    plt.plot(data['Frame'], data['X'], label='X Coordinate')
    plt.plot(data['Frame'], data['Y'], label='Y Coordinate')

    # バウンド地点を赤い点でプロット
    plt.scatter(list(frames_bounce), data.loc[data['Frame'].isin(frames_bounce), 'Y'], color='red', label='Bounces')

    plt.xlabel('Frame')
    plt.ylabel('Position')
    plt.legend()

    # グラフを保存するディレクトリを指定
    save_dir = './graphs/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # グラフを保存する際に、CSVファイルの名前を使用するように変更
    csv_file_name = os.path.basename(csv_file_path).split('.')[0]
    graph_file_name = f'{csv_file_name}_bounce_detection_graph.png'
    plt.savefig(os.path.join(save_dir, graph_file_name))

    # バウンド地点のフレーム番号を昇順で並び替えて出力
    print("バウンドが検出されたフレーム:", sorted(frames_bounce))

    plt.show()
else:
    print("ファイルが選択されませんでした。")

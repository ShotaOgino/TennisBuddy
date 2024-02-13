import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルを読み込む
df1 = pd.read_csv('/Users/shota/Coding/TennisBuddy/csv/2023_10_12_correct.csv')
df2 = pd.read_csv('/Users/shota/Coding/TennisBuddy/csv/2023_10_12_global.csv')

# df2の要素数をdf1に合わせる
df2 = df2.head(len(df1))

# プロットする
plt.plot(df1['Frame'], df1['Y'], 'o', label='2023_10_12_correct')
plt.plot(df2['Frame'], df2['Y'], 'o', label='2023_10_12_global')
""" 
plt.plot(df1['X'], df1['Frame'], label='2023_10_12_correct')
plt.plot(df2['X'], df2['Frame'], label='2023_10_12_global') """

# レジェンドを表示する
plt.legend()

# グラフを表示する
plt.show()

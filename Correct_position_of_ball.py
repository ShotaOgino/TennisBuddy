import cv2
import csv
import os

cap = None  # グローバル変数として定義

# マウスイベント時に処理を行う
def get_coordinates(event, x, y, flags, param):
    global frame_count, cap  # capをグローバル変数として扱う
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Frame: {}, X: {}, Y: {}'.format(frame_count, x, y))
        writer.writerow([frame_count, x, y])
        frame_count += 1  # マウスクリックでフレームカウントを増やす
        ret, frame = cap.read()  # マウスクリックで次のフレームを読み込む
        if ret:
            cv2.imshow('frame', frame)  # マウスクリックで次のフレームを表示する

# 動画ファイル名
video_file_name = '/Users/shota/Coding/TennisBuddy/input/2023_10_12.mp4'
# CSVファイル名
csv_file_name = './csv/' + os.path.splitext(os.path.basename(video_file_name))[0] + '_correct.csv'

# CSVファイルを開く
with open(csv_file_name, 'w', newline='') as file:
    global writer
    writer = csv.writer(file)
    writer.writerow(["Frame", "X", "Y"])

    # 動画を開く
    cap = cv2.VideoCapture(video_file_name)

    # ウィンドウにマウスイベントを追加
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', get_coordinates)

    global frame_count
    frame_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
            key = cv2.waitKey(0)  # 0を指定するとキー入力があるまで画像表示を停止します
            if key == ord(' '):
                frame_count += 1
                continue
            elif key == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

import argparse
import Models
import queue
import cv2
import csv
import numpy as np
from PIL import Image, ImageDraw
import os
import sys

import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()  # Tkのルートウィンドウを表示しない

    file_path = filedialog.askopenfilename()  # ファイル選択ダイアログを開く

    print("Selected file:", file_path)
    return file_path


#parse parameters
parser = argparse.ArgumentParser()
#parser.add_argument("--input_video_path", type=str)
#parser.add_argument("--output_video_path", type=str, default = "")
parser.add_argument("--save_weights_path", type = str , default="./weights/model.3")
parser.add_argument("--n_classes", type=int, default="256")

    
args = parser.parse_args()
#input_video_path =  args.input_video_path


input_video_path = select_file()

#input video pathの中身の名前部分を
# input_video_pathからファイル名を取得するには、os.path.basenameを使用します
output_video_path = "output/"+os.path.basename(input_video_path)

save_weights_path = args.save_weights_path
n_classes =  args.n_classes

print(input_video_path,output_video_path,save_weights_path,n_classes)

if output_video_path == "":
	#output video in same path
	output_video_path = input_video_path.split('.')[0] + "_TrackNet.mp4"

#get video fps&video size
video = cv2.VideoCapture(input_video_path)
fps = int(video.get(cv2.CAP_PROP_FPS))
output_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
output_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

#start from first frame
currentFrame = 0

#width and height in TrackNet
width , height = 640, 360
img, img1, img2 = None, None, None

#load TrackNet model
modelFN = Models.TrackNet.TrackNet
m = modelFN( n_classes , input_height=height, input_width=width   )
m.compile(loss='categorical_crossentropy', optimizer= 'adadelta' , metrics=['accuracy'])
m.load_weights(  save_weights_path  )

# In order to draw the trajectory of tennis, we need to save the coordinate of preious 7 frames 
q = queue.deque()
for i in range(0,8):
	q.appendleft(None)

#save prediction images as vidoe
#Tutorial: https://stackoverflow.com/questions/33631489/error-during-saving-a-video-using-python-and-opencv
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_video_path,fourcc, fps, (output_width,output_height))


#both first and second frames cant be predict, so we directly write the frames to output video
#capture frame-by-frame
video.set(1,currentFrame); 
ret, img1 = video.read()

#write image to video
output_video.write(img1)
currentFrame +=1
#resize it 
img1 = cv2.resize(img1, ( width , height ))
#input must be float type
img1 = img1.astype(np.float32)

if img1 is None:
    raise ValueError(f"Failed to read a frame from the video at frame index {currentFrame}. Check if the video file is accessible and valid.")


#capture frame-by-frame
video.set(1,currentFrame)
ret, img = video.read()
#write image to video
output_video.write(img)
currentFrame +=1
#resize it 
img = cv2.resize(img, ( width , height ))
#input must be float type
img = img.astype(np.float32)

""" # CSVファイルのパスを指定
# '\\' で分割して、最後の要素を取得
last_part = input_video_path.split('\\')[-1]

#csv_file_path = "./csv/"+last_part.replace(".mp4",".csv")
#csv_file = open(csv_file, mode='w', newline='')  # CSVファイルをオープン

csv_file_path="./csv/BetweenPoint1.csv"
csv_file = open(csv_file_path, mode='w', newline='')  # CSVファイルをオープン """

# os.path.sepを使用すると、OSに依存しないパス区切り文字を扱えます
last_part = input_video_path.split(os.path.sep)[-1]

# 拡張子をチェックし、必要に応じて置換
if last_part.lower().endswith('.mp4'):
    csv_file_name = last_part[:-4] + '.csv'  # '.mp4' を '.csv' に置換
elif last_part.lower().endswith('.mov'):
    csv_file_name = last_part[:-4] + '.csv'  # '.MOV' を '.csv' に置換
else:
    raise ValueError("Unsupported file format. Please provide a .mp4 or .MOV file.")

# CSVファイルパスを構築
csv_file_path = os.path.join(".", "csv", csv_file_name)

# CSVファイルをオープン
csv_file = open(csv_file_path, mode='w', newline='')

# CSVファイルにヘッダーを書き込み（x座標とy座標のカラム）
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame', 'X', 'Y'])

# ビデオの総フレーム数を取得
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total: 
        print()

# 処理されたフレーム数
processed_frames = 0

while(True):
    

	img2 = img1
	img1 = img

	#capture frame-by-frame
	video.set(1,currentFrame); 
	ret, img = video.read()

	#if there dont have any frame in video, break
	if not ret: 
		print("Failed to read frame")
		break

	#img is the frame that TrackNet will predict the position
	#since we need to change the size and type of img, copy it to output_img
	output_img = img

	#resize it 
	img = cv2.resize(img, ( width , height ))
	#input must be float type
	img = img.astype(np.float32)


	#combine three imgs to  (width , height, rgb*3)
	X =  np.concatenate((img, img1, img2),axis=2)

	#since the odering of TrackNet  is 'channels_first', so we need to change the axis
	X = np.rollaxis(X, 2, 0)
	#prdict heatmap
	pr = m.predict(np.array([X]), verbose=0)[0]

	#since TrackNet output is ( net_output_height*model_output_width , n_classes )
	#so we need to reshape image as ( net_output_height, model_output_width , n_classes(depth) )
	#.argmax( axis=2 ) => select the largest probability as class
	pr = pr.reshape(( height ,  width , n_classes ) ).argmax( axis=2 )

	#cv2 image must be numpy.uint8, convert numpy.int64 to numpy.uint8
	pr = pr.astype(np.uint8) 

	#reshape the image size as original input image
	heatmap = cv2.resize(pr  , (output_width, output_height ))

	#heatmap is converted into a binary image by threshold method.
	ret,heatmap = cv2.threshold(heatmap,127,255,cv2.THRESH_BINARY)

	#find the circle in image with 2<=radius<=7
	circles = cv2.HoughCircles(heatmap, cv2.HOUGH_GRADIENT,dp=1,minDist=1,param1=50,param2=2,minRadius=2,maxRadius=7)

	#In order to draw the circle in output_img, we need to used PIL library
	#Convert opencv image format to PIL image format
	PIL_image = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)   
	PIL_image = Image.fromarray(PIL_image)

	#check if there have any tennis be detected
	if circles is not None:
		#if only one tennis be detected
		if len(circles) == 1:

			x = int(circles[0][0][0])
			y = int(circles[0][0][1])
			#print(currentFrame, x,y)

			# ボールの位置情報をCSVファイルに書き込む
			csv_writer.writerow([currentFrame, x, y])

			#push x,y to queue
			q.appendleft([x,y])   
			#pop x,y from queue
			q.pop()    
		else:
			# ボールが検出されなかった場合、Noneを書き込む
			csv_writer.writerow([currentFrame, None, None])
			#push None to queue
			q.appendleft(None)
			#pop x,y from queue
			q.pop()
	else:
		# ボールが検出されなかった場合、Noneを書き込む
		csv_writer.writerow([currentFrame, None, None])
		#push None to queue
		q.appendleft(None)
		#pop x,y from queue
		q.pop()

	#draw current frame prediction and previous 7 frames as yellow circle, total: 8 frames
	for i in range(0,8):
		if q[i] is not None:
			draw_x = q[i][0]
			draw_y = q[i][1]
			hello=5
			bbox =  (draw_x - hello, draw_y - hello, draw_x + hello, draw_y + hello)
			draw = ImageDraw.Draw(PIL_image)
			draw.ellipse(bbox, outline ='yellow')
			del draw

	#Convert PIL image format back to opencv image format
	opencvImage =  cv2.cvtColor(np.array(PIL_image), cv2.COLOR_RGB2BGR)
	#write image to output_video
	output_video.write(opencvImage)

	#next frame
	currentFrame += 1

	# フレーム処理後 
	processed_frames += 1
	print_progress_bar(processed_frames, total_frames, prefix='Progress:', suffix='Complete', length=50)


# CSVファイルをクローズ
csv_file.close()

# everything is done, release the video
video.release()
output_video.release()
print("finish")


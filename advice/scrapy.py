from googleapiclient.discovery import build
import os
import csv
import speech_recognition as sr
from pydub import AudioSegment
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from pytube import YouTube
from moviepy.editor import *

# APIキーの設定（あなたのAPIキーに置き換えてください）
api_key = 'AIzaSyBhSaj0X13njXD-QeKNlzmt5RDvwU2CcaE'
youtube = build('youtube', 'v3', developerKey=api_key)

# チャンネルIDの取得（Patrick MouratoglouのチャンネルID）
channel_id = 'UCnN1Rj2OtO67OIUimR18KWg'  # ここにPatrick MouratoglouのチャンネルIDを入力

def get_channel_videos(channel_id):
    # チャンネルの動画リストを取得
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    
    if 'items' in res:
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        print("Error: 'items' not found in the response")
        return

    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50, pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos

# 音声をテキストに変換する関数
def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    return text

# テキストからメインポイントを抽出する関数
def extract_main_points(text):
    words = word_tokenize(text)
    freq_dist = FreqDist(words)
    main_points = freq_dist.most_common(10)  # ここでは最も頻繁に出現する10語をメインポイントとしています
    return main_points

# YouTube動画から音声をダウンロードし、そのファイル名を返す関数
def download_audio(video_url):
    # YouTube動画をダウンロード
    youtube = YouTube(video_url)
    video = youtube.streams.first()
    video.download(output_path="temp", filename="temp_video")

    # Check if the video was downloaded correctly
    if not os.path.exists("temp/temp_video.mp4"):
        print("Error: Video download failed or file was saved in a different location.")
        return

    # ダウンロードした動画から音声を抽出
    video_clip = VideoFileClip("temp/temp_video.mp4")
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("temp/temp_audio.mp3")

    # 音声ファイルの名前を返す
    return "temp/temp_audio.mp3"

# チャンネルの動画リンクを取得
videos = get_channel_videos(channel_id)

# CSVファイルに書き込む
with open('videos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Video ID", "Video Link", "Main Points"])  # ヘッダーを書き込む

    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_link = f"https://www.youtube.com/watch?v={video_id}"

        # 音声をテキストに変換
        audio_file = download_audio(video_link)
        if audio_file is None:
            continue
        text = transcribe_audio(audio_file)

        # メインポイントを抽出
        main_points = extract_main_points(text)

        writer.writerow([video_id, video_link, main_points])  # 動画ID、リンク、メインポイントを書き込む

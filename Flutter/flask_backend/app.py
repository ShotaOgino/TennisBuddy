import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/upload/*": {"origins": "*"}})
UPLOAD_FOLDER = './uploads'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return 'ファイルが見つかりません', 400

    video = request.files['video']

    # uploads ディレクトリの存在確認と作成
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # ファイル名の衝突を避けるための処理が必要 (例: ファイル名にタイムスタンプを追加)
    filepath = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(filepath)

    return 'ファイルがアップロードされました', 200

@app.route('/')
def index():
    return 'Welcome to the Flask App!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
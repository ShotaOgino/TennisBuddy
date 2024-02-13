# Debianベースのイメージを使用
FROM debian:buster

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y curl git unzip xz-utils zip libglu1-mesa wget

# Flutter SDKのインストール
RUN git clone https://github.com/flutter/flutter.git /flutter
ENV PATH="/flutter/bin:/flutter/bin/cache/dart-sdk/bin:${PATH}"

# 作業ディレクトリの設定
WORKDIR /app

# Flutter doctorの実行
RUN flutter doctor

# ポートの公開（Flutterのデフォルトウェブポート）
EXPOSE 8080

# アプリの起動コマンド
CMD ["flutter", "run", "-d", "web-server", "--web-port", "8080", "--web-hostname", "0.0.0.0"]

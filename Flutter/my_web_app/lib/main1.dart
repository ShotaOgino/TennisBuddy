import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Tennis Buddy'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Container(
                width: MediaQuery.of(context).size.width * 0.8, // 画面幅の80%に設定
                height: MediaQuery.of(context).size.height * 0.4, // 画面高さの40%に設定
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      icon: Icon(Icons.add, size: 50),
                      onPressed: () async {
                        FilePickerResult? result = await FilePicker.platform.pickFiles(
                          type: FileType.video,
                        );
                        if (result != null) {
                          // 選択されたファイルの処理 (例: ファイルのパスを使用)
                          // PlatformFile file = result.files.first;
                        } else {
                          // ユーザーがファイル選択をキャンセルした場合の処理
                        }
                      },
                    ),
                    //Text('動画を追加'),
                  ],
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  // 送信ボタンの処理をここに書く
                },
                style: ElevatedButton.styleFrom(
                  primary: Colors.green,
                  padding: EdgeInsets.symmetric(horizontal: 50, vertical: 20),
                ),
                child: Text('送信'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
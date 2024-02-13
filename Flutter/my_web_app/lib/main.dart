import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String? _videoFileName; // 選択された動画のファイル名を保存
  Uint8List? _fileBytes; // 選択された動画のバイトデータを保存

  void _pickVideo() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
    );
    if (result != null) {
      setState(() {
        _videoFileName = result.files.single.name;
        _fileBytes = result.files.first.bytes; // バイトデータを保存
      });
      debugPrint('選択された動画のファイル名: $_videoFileName');
    }
  }

  /* void _uploadVideo() async {
    if (_fileBytes != null && _videoFileName != null) {
      var uri = Uri.parse('http://127.0.0.1:5000/upload');
      var request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes(
          'video',
          _fileBytes!,
          filename: _videoFileName!,
        ));

      var response = await request.send();

      if (response.statusCode == 200) {
        print('動画がアップロードされました');
      } else {
        print('アップロードに失敗しました');
      }
    }
  } */

  void _uploadVideo() async {
  if (_fileBytes != null && _videoFileName != null) {
    var uri = Uri.parse('http://127.0.0.1:5000/upload');
    var request = http.MultipartRequest('POST', uri)
      ..files.add(http.MultipartFile.fromBytes(
        'video',
        _fileBytes!,
        filename: _videoFileName!,
      ));

    // 送信を開始する前にコンソールにメッセージを出力
    print('送信中...');

    var response = await request.send();

    if (response.statusCode == 200) {
      print('動画がアップロードされました');
    } else {
      print('アップロードに失敗しました');
    }

    // 送信が完了した後にコンソールにメッセージを出力
    print('送信！');
  } else {
    // ファイルが選択されていない場合のメッセージ
    print('ファイルが選択されていません');
  }
}


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
                width: MediaQuery.of(context).size.width * 0.8,
                height: MediaQuery.of(context).size.height * 0.4,
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _videoFileName == null
                        ? IconButton(
                            icon: Icon(Icons.add, size: 50),
                            onPressed: _pickVideo,
                          )
                        : Text(_videoFileName!), // 選択されたファイル名を表示
                  ],
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _uploadVideo,
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

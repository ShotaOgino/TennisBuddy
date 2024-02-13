import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:minio/minio.dart';
import 'dart:convert'; // for utf8
import 'dart:typed_data'; // for Uint8List

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: FileUploadWidget(),  // あなたのウィジェットをここに置く
    );
  }
}


class FileUploadWidget extends StatefulWidget {
  @override
  _FileUploadWidgetState createState() => _FileUploadWidgetState();
}

class _FileUploadWidgetState extends State<FileUploadWidget> {
  File? _file;

  // Minioクライアントの初期化（安全な方法で認証情報を扱ってください）
  final minio = Minio(
    endPoint: 's3-ap-northeast-1.amazonaws.com',
    accessKey: '', // 実際のキーを直接コードに含めないでください
    secretKey: '', // 実際のキーを直接コードに含めないでください
  );

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.video);

    if (result != null) {
      setState(() {
        _file = File(result.files.single.path!);
      });
    }
  }

  Future<void> _uploadFile() async {
  if (_file == null) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('ファイルを選択してください。'),
    ));
    return;
  }

  try {
    final fileStream = _file!.openRead().cast<Uint8List>(); // ここで型変換を行う
    /* final fileSize = await _file!.length(); // ファイルサイズを取得 */

    // Minioを使用してファイルをアップロード
    await minio.putObject('swinganalysis', 'object-name', fileStream);

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('ファイルをアップロードしました。'),
    ));
  } catch (e) {
    print(e);
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('アップロードに失敗しました。'),
    ));
  }
}

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: _pickFile,
          child: Text('ファイルを選択'),
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: _uploadFile,
          child: Text('送信'),
          style: ElevatedButton.styleFrom(primary: Colors.green),
        ),
      ],
    );
  }
}

/* import 'package:flutter/material.dart';
import 'image_from_s3.dart'; // 1でインポートしたファイル

void main() {
  runApp(App());
}

class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ImageFromS3(), // ImageFromS3 ウィジェットを使用
    );
  }
} */


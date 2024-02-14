/* import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:cross_file/cross_file.dart';
import 'package:desktop_drop/desktop_drop.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;
import 'package:upload_with_presigned_url/network_service.dart';
import 'package:upload_with_presigned_url/upload_data_request_model.dart';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 's3_class_path.dart';

class UploadFileView extends StatefulWidget {
  const UploadFileView({Key? key}) : super(key: key);

  @override
  _UploadFileViewState createState() => _UploadFileViewState();
}

class _UploadFileViewState extends State<UploadFileView> {
  bool isDragging = false;
  ValueNotifier<Object?> selectedFile = ValueNotifier<Object?>(null);
  NetworkService networkService = NetworkService();
  UploadData? uploadData;

  @override
  void initState() {
    super.initState();
    loadUploadData();
    dotenv.load();  // 環境変数を読み込む
  }

  Future<void> loadUploadData() async {
    final jsonString = await rootBundle.loadString('../assets/config/upload_config.json');
    final Map<String, dynamic> jsonMap = json.decode(jsonString);
    setState(() {
      uploadData = UploadData(
        url: jsonMap['url'],
        fields: Map<String, String>.from(jsonMap['fields']),
      );
    });
  }

  void uploadSelectedFile() async {
    if (uploadData == null) return;

    final minio = S3.instance.getMinio();
    final (selectedFileBytes, selectedFileName) = await getFileBytesAndName(selectedFile.value);

    // Minioを使用してファイルをアップロード
    try {
      await minio.putObject(
        dotenv.env['BUCKET_NAME']!,  // .envからバケット名を読み込む
        selectedFileName,
        selectedFileBytes,
      );
      // アップロード成功時の処理
    } catch (e) {
      // エラー処理
      print(e);
    }
  }

  Future<(List<int>, String)> getFileBytesAndName(Object? file) async {
    List<int> bytes;
    String fileName;

    if (file is XFile) {
      bytes = await file.readAsBytes();
      fileName = file.name;
    } else if (file is PlatformFile) {
      bytes = kIsWeb ? file.bytes! : await File(file.path!).readAsBytes();
      fileName = file.name;
    } else {
      throw Exception('Invalid file type');
    }
    return (bytes, fileName);
  }

  Future<void> _selectFile() async {
    final result = await FilePicker.platform.pickFiles(
      allowMultiple: false,
      type: FileType.custom,
      allowedExtensions: ['mp4', 'mov', 'avi'],
    );

    if (result != null && result.files.isNotEmpty) {
      selectedFile.value = result.files.single;
    }
  }

  void _onDragDone(DropDoneDetails details) {
    final droppedFile = details.files.first;
    final selectedFileType = path.extension(droppedFile.name).toLowerCase();

    const allowedVideoExtensions = ['.mp4', '.mov', '.avi'];
    if (!allowedVideoExtensions.contains(selectedFileType)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a valid video file type'), backgroundColor: Colors.red),
      );
      return;
    }

    selectedFile.value = droppedFile;
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final double boxWidth = min(width * 0.8, 500);

    return Scaffold(
      appBar: AppBar(title: Text('Upload File')),
      body: Center(
        child: DropTarget(
          onDragDone: _onDragDone,
          onDragEntered: (_) => setState(() => isDragging = true),
          onDragExited: (_) => setState(() => isDragging = false),
          child: Container(
            height: 300,
            width: boxWidth,
            decoration: BoxDecoration(
              color: isDragging ? Colors.deepPurple.shade300 : Colors.deepPurple,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Center(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.upload_file, size: 32, color: Colors.white),
                  SizedBox(height: 10),
                  Text('Upload Data File', style: TextStyle(color: Colors.white, fontSize: 20)),
                  SizedBox(height: 8),
                  Text('Drag and drop your data file here', style: TextStyle(color: Colors.white, fontSize: 16)),
                  SizedBox(height: 8),
                  Text('or', style: TextStyle(color: Colors.white, fontSize: 16)),
                  SizedBox(height: 8),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32.0),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(8),
                        color: Colors.white,
                      ),
                      padding: const EdgeInsets.all(4),
                      child: Row(
                        children: [
                          ElevatedButton(
                            onPressed: _selectFile,
                            child: const Text('Select File'),
                          ),
                          SizedBox(width: 16),
                          ValueListenableBuilder<Object?>(
                            valueListenable: selectedFile,
                            builder: (context, file, _) {
                              final fileName = file is XFile
                                  ? file.name
                                  : file is PlatformFile
                                      ? file.name
                                      : "No file selected";
                              return Text(fileName, style: const TextStyle(color: Colors.deepPurple));
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  SizedBox(height: 16),
                  ValueListenableBuilder<Object?>(
                    valueListenable: selectedFile,
                    builder: (context, file, _) {
                      return ElevatedButton(
                        onPressed: file == null ? null : uploadSelectedFile,
                        child: const Text('Upload File', style: TextStyle(color: Colors.white)),
                        style: ElevatedButton.styleFrom(primary: file == null ? Colors.grey[300] : Colors.lightGreen),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
 */


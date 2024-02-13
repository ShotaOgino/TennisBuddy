import 'package:flutter/material.dart';
import 'package:minio_new/minio.dart';
import 'dart:typed_data';
import 'dart:convert';

final configFile = File('config.json');
final config = json.decode(configFile.readAsStringSync());

class ImageFromS3 extends StatelessWidget {
  ImageFromS3({super.key});

  final minio = Minio(
    endPoint: 's3-ap-northeast-1.amazonaws.com',
    region: 'ap-northeast-1',
    accessKey: config['accessKey'],
    secretKey: config['secretKey'],
  );

  Future<Image> getImage() async {
    final stream = await minio.getObject('swinganalysis', 'logo.jpg');
    List<int> memory = [];
    await for (var value in stream) {
      memory.addAll(value);
    }
    return Image.memory(Uint8List.fromList(memory));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('タイトル')),
      body: Center(
        child: FutureBuilder(
          future: getImage(),
          builder: (BuildContext context, AsyncSnapshot<Image> snapshot) {
            if (snapshot.hasData) {
              return Center(child: snapshot.data);
            } else {
              return const Center(
                child: Text('データが取得できていません'),
              );
            }
          },
        ),
      ),
    );
  }
}
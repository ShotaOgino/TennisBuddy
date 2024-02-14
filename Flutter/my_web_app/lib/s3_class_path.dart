import 'package:flutter_dotenv/flutter_dotenv.dart';  // 環境変数を扱う
import 'package:minio_new/minio.dart';     // Minioクライアント

class S3 {
  Minio? _minio;
  S3._();

  static final instance = S3._();
  Minio getMinio(){
      _minio ??= Minio(
        endPoint: dotenv.env['END_POINT']!,
        region: dotenv.env['REGION']!,
        accessKey: dotenv.env['ACCESS_KEY']!,
        secretKey: dotenv.env['SECRET_KEY']!,
        useSSL: true,
      );
    return _minio!;
  }
}
import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Expanded(
          // ローカルの動画代わりの画像
          child: Image.asset('assets/tennis_video_placeholder.png'), // 画像ファイル名に置き換えてください
        ),
        Expanded(
          // ローカルの3Dモデル代わりの画像
          child: Image.asset('assets/three_js_placeholder.png'), // 画像ファイル名に置き換えてください
        ),
      ],
    );
  }
}

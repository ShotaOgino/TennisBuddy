import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:snippet_coder_utils/FormHelper.dart';
import 'package:snippet_coder_utils/multi_images_utils.dart';
import 'package:flutter_progress_hud/flutter_progress_hud.dart';


class S3UploadPage extends StatefulWidget {
  const S3UploadPage({super.key});

  @override
  State<S3UploadPage> createState() => _S3UploadPage();
}

class _S3UploadPage extends State<S3UploadPage>{
  bool isApiCallprocess = false;
  String singleImageFile = "";
  List<String> selectedMultiImages = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("S3 Uploading"),
      ),
      body: ProgressHUD(
        child: uploadUI(),
        //inAsyncCall: isApiCallprocess,
        backgroundColor: Colors.black.withOpacity(0.3),
        //opacity: .3,
        //key: UniqueKey(),
      ),
    );
  }

  uploadUI(){
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          "Single Image",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        SizedBox(
          child: MultiImagePicker(
            totalImages: 1,
            imageSource: ImagePickSource.gallery,
            onImageChanged: (images){
              singleImageFile = images[0].imageFile;
            },
          ),
        ),
        Text(
          "Multi Image",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        SizedBox(
          child: MultiImagePicker(
            totalImages: 5,
            imageSource: ImagePickSource.gallery,
            onImageChanged: (images){
              selectedMultiImages = [];
              images.forEach(
                (image) {
                  if(image is ImageUploadModel){
                    selectedMultiImages.add(image.imageFile);
                  }
                }
              );
              singleImageFile = images[0].imageFile;
            },
          ),
        ),

        Center(
          child: FormHelper.submitButton(
            "Upload",
            () {

            },
            btnColor: Colors.redAccent,
            borderColor: Colors.redAccent,
            txtColor: Colors.white,
            borderRadius: 10,
          ),
        )
      ],
    );
  }
}
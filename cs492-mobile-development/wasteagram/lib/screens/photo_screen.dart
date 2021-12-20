import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'crash_screen.dart';
import 'new_entry_screen.dart';
import 'take_photo_screen.dart';
import '/components/custom_app_bar.dart';

class PhotoScreen extends StatefulWidget {
  final CameraDescription camera;
  const PhotoScreen({Key? key, required this.camera}) : super(key: key);

  @override
  _PhotoScreenState createState() => _PhotoScreenState();
}

class _PhotoScreenState extends State<PhotoScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: Drawer(child: CrashScreen()),
      appBar: CustomAppBar(),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
            child: Semantics(
              button: true,
              enabled: true,
              onTapHint: 'take a new photo with camera',
              child: ElevatedButton(
                child: Icon(
                  Icons.camera,
                  size: 48.0,
                ),
                onPressed: () => takeNewImage(context),
              ),
            ),
          ),
          Center(child: Text('Camera')),
          Container(height: 10.0),
          Center(
            child: Semantics(
              button: true,
              enabled: true,
              onTapHint: 'choose an existing photo from gallery',
              child: ElevatedButton(
                child: Icon(
                  Icons.image_search,
                  size: 48.0,
                ),
                onPressed: () => getExistingImage(context),
              ),
            ),
          ),
          Center(child: Text('Gallery')),
        ],
      ),
    );
  }

  void getExistingImage(BuildContext context) async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    final image = File(pickedFile!.path);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (context) {
          return NewEntryScreen(image: image);
        },
      ),
    );
  }

  void takeNewImage(BuildContext context) async {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) {
          return TakePhotoScreen(camera: widget.camera);
        },
      ),
    );
  }
}

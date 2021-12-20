import 'dart:io';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:location/location.dart';
import 'crash_screen.dart';
import '/components/custom_app_bar.dart';
import '../models/food_waste_post_dto.dart';

class NewEntryScreen extends StatefulWidget {
  final File image;
  NewEntryScreen({Key? key, required this.image}) : super(key: key);

  @override
  _NewEntryScreenState createState() => _NewEntryScreenState();
}

class _NewEntryScreenState extends State<NewEntryScreen> {
  late FoodWastePostDTO postDTO;
  final _formKey = GlobalKey<FormState>();
  late Future imageURLFuture;

  @override
  void initState() {
    super.initState();
    postDTO = FoodWastePostDTO.isEmpty();
    imageURLFuture = uploadImage();
    retrieveLocation();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: Drawer(child: CrashScreen()),
      appBar: CustomAppBar(),
      body: FutureBuilder(
        future: imageURLFuture,
        builder: (context, snapshot) {
          // handle case where future has resolved
          if (snapshot.hasData) {
            setImageURL(snapshot.data.toString());
            return Column(
              children: [
                imageContainer(context, postDTO.imageURL),
                quantityForm(context),
                Flexible(child: Container()),
                uploadButton(context),
              ],
            );
          }
          // handle case where future is still waiting
          return Center(child: CircularProgressIndicator());
        },
      ),
    );
  }

  Widget uploadButton(BuildContext context) {
    return Align(
      alignment: Alignment.bottomCenter,
      child: Container(
        color: Colors.blue,
        height: MediaQuery.of(context).size.height * 0.10,
        width: MediaQuery.of(context).size.width,
        child: Semantics(
          button: true,
          enabled: true,
          onTapHint: 'upload food waste post',
          child: TextButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                _formKey.currentState!.save();
                setDate();
                saveToDatabase();
                Navigator.of(context).pop();
              }
            },
            child: Text('Upload', style: Theme.of(context).textTheme.headline4),
          ),
        ),
      ),
    );
  }

  Widget quantityForm(BuildContext context) {
    return Form(
      key: _formKey,
      child: TextFormField(
        keyboardType: TextInputType.number,
        textAlign: TextAlign.center,
        decoration: InputDecoration(hintText: '# of Items'),
        style: Theme.of(context).textTheme.headline6,
        validator: (value) => quantityValidator(value),
        onSaved: (value) => setQuantity(int.parse(value!)),
      ),
    );
  }

  Widget imageContainer(BuildContext context, String imageURL) {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: MediaQuery.of(context).size.height * 0.4,
      child: Padding(
        padding: EdgeInsets.all(5),
        child: Semantics(
          image: true,
          hint: 'image representing chosen photo',
          child: Image.network(imageURL),
        ),
      ),
    );
  }

  void saveToDatabase() {
    FirebaseFirestore.instance.collection('posts').add({
      'date': postDTO.date,
      'imageURL': postDTO.imageURL,
      'latitude': postDTO.latitude,
      'longitude': postDTO.longitude,
      'quantity': postDTO.quantity
    });
  }

  Future uploadImage() async {
    var fileName = DateTime.now().toString() + '.jpg';
    Reference storageReference = FirebaseStorage.instance.ref().child(fileName);
    UploadTask uploadTask = storageReference.putFile(widget.image);
    await uploadTask;
    final url = await storageReference.getDownloadURL();
    return url;
  }

  void retrieveLocation() async {
    var locationService = Location();
    try {
      // check whether location services are enabled
      var _serviceEnabled = await locationService.serviceEnabled();
      // request service if it is not enabled
      if (!_serviceEnabled) {
        _serviceEnabled = await locationService.requestService();
        // handle case where request is denied
        if (!_serviceEnabled) {
          print('Failed to enable service. Returning.');
          return;
        }
      }

      // check whether permissions have been granted
      var _permissionGranted = await locationService.hasPermission();
      // handle case where permissions have not already been granted
      if (_permissionGranted == PermissionStatus.denied) {
        // request permission
        _permissionGranted = await locationService.requestPermission();
        // handle case where request is denied
        if (_permissionGranted != PermissionStatus.granted) {
          print('Location service permission not granted. Returning.');
          return;
        }
      }

      final locationData = await locationService.getLocation();
    }
    // handle potential exception
    on PlatformException catch (e) {
      print('Error: ${e.toString()}, code: ${e.code}');
      return;
    }

    // handle case where service enabled, permission granted, and no error
    final locationData = await locationService.getLocation();
    postDTO.latitude = locationData.latitude;
    postDTO.longitude = locationData.longitude;
  }

  void setDate() => postDTO.date = DateTime.now();
  void setQuantity(int quantity) => postDTO.quantity = quantity;
  void setImageURL(String url) => postDTO.imageURL = url;
  void setLocation(Map locationMap) {
    postDTO.latitude = locationMap['latitude'];
    postDTO.longitude = locationMap['longitude'];
  }

  quantityValidator(value) {
    if (value == null || value.isEmpty) {
      return 'Please enter a number of wasteful items';
    } else if (int.parse(value) < 0) {
      return 'Number of wasteful items can\'t be negative';
    } else {
      return null;
    }
  }
}

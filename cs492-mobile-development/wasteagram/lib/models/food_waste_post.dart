import 'package:cloud_firestore/cloud_firestore.dart';

class FoodWastePost {
  // fields
  late DateTime date;
  late String imageURL;
  late double latitude;
  late double longitude;
  late int quantity;

  // constructors
  FoodWastePost(
      {required this.date,
      required this.imageURL,
      required this.latitude,
      required this.longitude,
      required this.quantity});

  FoodWastePost.fromSnapshotMap(
      QueryDocumentSnapshot<Map<String, dynamic>> doc) {
    date = doc['date'].toDate();
    imageURL = doc['imageURL'];
    quantity = doc['quantity'];
    latitude = doc['latitude'];
    longitude = doc['longitude'];
  }

  FoodWastePost.fromDartMap(map) {
    date = map['date'];
    imageURL = map['imageURL'];
    quantity = map['quantity'];
    latitude = map['latitude'];
    longitude = map['longitude'];
  }
}

import 'package:badges/badges.dart';
import 'package:camera/camera.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_analytics/observer.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'crash_screen.dart';
import 'detail_screen.dart';
import 'photo_screen.dart';
import '/components/custom_app_bar.dart';
import '/models/food_waste_post.dart';

class ListScreen extends StatefulWidget {
  final CameraDescription camera;
  final FirebaseAnalytics analytics;
  final FirebaseAnalyticsObserver observer;
  const ListScreen(
      {Key? key,
      required this.camera,
      required this.analytics,
      required this.observer})
      : super(key: key);

  @override
  _ListScreenState createState() => _ListScreenState(analytics, observer);
}

class _ListScreenState extends State<ListScreen> {
  _ListScreenState(this.analytics, this.observer);

  final FirebaseAnalytics analytics;
  final FirebaseAnalyticsObserver observer;
  late int totalQuantity;
  Stream<QuerySnapshot<Map<String, dynamic>>> dbStream = FirebaseFirestore
      .instance
      .collection('posts')
      .orderBy('date', descending: true)
      .snapshots();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
      stream: dbStream,
      builder: (context,
          AsyncSnapshot<QuerySnapshot<Map<String, dynamic>>> snapshot) {
        if (!snapshot.hasData) {
          return loadingScaffold();
        } else if (snapshot.data == null) {
          return Text('data snapshot.data is null');
        } else if (snapshot.hasData && snapshot.data!.docs.length > 0) {
          int total = getTotalQuantity(snapshot.data!.docs);
          return Scaffold(
            endDrawer: Drawer(child: CrashScreen()),
            appBar: CustomAppBar(title: 'Wastegram - ${total}'),
            body: postList(snapshot, context),
            floatingActionButton: addPostButton(),
            floatingActionButtonLocation:
                FloatingActionButtonLocation.centerFloat,
          );
        }
        return Text('something else happened');
      },
    );
  }

  Widget addPostButton() {
    return Semantics(
      button: true,
      enabled: true,
      onTapHint: 'add new food waste post',
      child: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () => pushPhotoScreen(context),
      ),
    );
  }

  Widget loadingScaffold() {
    return Scaffold(
      appBar: CustomAppBar(title: 'Wastegram - Loading...'),
      body: Center(child: CircularProgressIndicator()),
    );
  }

  int getTotalQuantity(List docs) {
    int total = 0;
    docs.forEach((doc) {
      num currNum = doc['quantity'];
      int currInt = currNum.toInt();
      total += currInt;
    });
    return total;
  }

  Widget postList(AsyncSnapshot<QuerySnapshot<Map<String, dynamic>>> snapshot,
      BuildContext context) {
    return ListView.builder(
      itemCount: snapshot.data!.docs.length,
      itemBuilder: (context, index) {
        final currDoc = snapshot.data!.docs[index];
        FoodWastePost post = FoodWastePost.fromSnapshotMap(currDoc);
        return postTile(snapshot, context, post);
      },
    );
  }

  Widget postTile(AsyncSnapshot<QuerySnapshot<Map<String, dynamic>>> snapshot,
      BuildContext context, FoodWastePost post) {
    return GestureDetector(
      onTap: () => pushDetailScreen(context, post),
      child: ListTile(
        title: Text(
          '${DateFormat.yMMMMEEEEd().format(post.date)}',
        ),
        trailing: Badge(
          badgeColor: Colors.redAccent,
          shape: BadgeShape.square,
          borderRadius: BorderRadius.circular(2),
          badgeContent: Text('${post.quantity}'),
        ),
      ),
    );
  }

  void pushDetailScreen(BuildContext context, FoodWastePost post) async {
    await widget.analytics.logEvent(
        name: 'details_page_visited',
        parameters: <String, dynamic>{
          'post_date': post.date.toString(),
          'post_quantity': post.quantity
        });
    Navigator.of(context).push(MaterialPageRoute(builder: (context) {
      return DetailScreen(post: post);
    }));
  }

  void pushPhotoScreen(BuildContext context) async {
    await widget.analytics.logEvent(
        name: 'new_entry_engaged',
        parameters: <String, dynamic>{
          'date_started': DateTime.now().toString()
        });
    Navigator.of(context).push(MaterialPageRoute(builder: (context) {
      return PhotoScreen(camera: widget.camera);
    }));
  }
}

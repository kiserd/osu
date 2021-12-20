import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'crash_screen.dart';
import '/components/custom_app_bar.dart';
import '/models/food_waste_post.dart';

class DetailScreen extends StatelessWidget {
  final FoodWastePost post;
  DetailScreen({Key? key, required this.post}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: Drawer(child: CrashScreen()),
      appBar: CustomAppBar(),
      body: Padding(
        padding: const EdgeInsets.all(5.0),
        child: Column(
          children: [
            Padding(
              padding: EdgeInsets.all(5.0),
              child: Text('${DateFormat.yMMMMEEEEd().format(post.date)}',
                  style: Theme.of(context).textTheme.headline5),
            ),
            imageComponent(context),
            Padding(
              padding: EdgeInsets.all(5.0),
              child: Text('${post.quantity} Items',
                  style: Theme.of(context).textTheme.headline4),
            ),
            Padding(
              padding: EdgeInsets.all(5.0),
              child: Text('Location: (${post.latitude}, ${post.longitude})',
                  style: Theme.of(context).textTheme.subtitle2),
            ),
          ],
        ),
      ),
    );
  }

  Widget imageComponent(BuildContext context) {
    return Flexible(
      child: FractionallySizedBox(
        heightFactor: 0.4,
        widthFactor: 1,
        child: Semantics(
          image: true,
          hint: 'image for selected food waste post',
          child: Image.network(
            post.imageURL,
            loadingBuilder: (BuildContext context, Widget child,
                ImageChunkEvent? loadingProgress) {
              if (loadingProgress == null) {
                return child;
              } else {
                return Center(child: CircularProgressIndicator());
              }
            },
          ),
        ),
      ),
    );
  }
}

import 'package:camera/camera.dart';
import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_analytics/observer.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import '/screens/list_screen.dart';

class App extends StatelessWidget {
  final CameraDescription camera;
  static FirebaseAnalytics analytics = FirebaseAnalytics();
  static FirebaseAnalyticsObserver observer =
      FirebaseAnalyticsObserver(analytics: analytics);
  const App({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData.dark(),
      navigatorObservers: <NavigatorObserver>[observer],
      home: ListScreen(
        camera: this.camera,
        analytics: analytics,
        observer: observer,
      ),
    );
  }
}

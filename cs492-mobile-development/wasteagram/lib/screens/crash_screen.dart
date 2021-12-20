import 'package:flutter/material.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

class CrashScreen extends StatelessWidget {
  const CrashScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(5),
      child: ListView(
        children: [
          ListTile(title: Text('Force Crash Screen')),
          ListTile(
            title: Text('Click Icon to Force Crash'),
            trailing: GestureDetector(
              child: Icon(Icons.delete),
              onTap: () => FirebaseCrashlytics.instance.crash(),
            ),
          ),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';

class CustomAppBar extends StatelessWidget with PreferredSizeWidget {
  final String title;
  const CustomAppBar({Key? key, this.title: 'Wastegram'}) : super(key: key);

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      leading: (ModalRoute.of(context)?.canPop ?? false) ? BackButton() : null,
      centerTitle: true,
      title: Text(
        '${this.title}',
      ),
      actions: [
        Align(
          alignment: Alignment.centerRight,
          child: IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {
              Scaffold.of(context).openEndDrawer();
            },
          ),
        )
      ],
    );
  }
}

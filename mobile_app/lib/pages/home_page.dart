import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {

    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Select a bar',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.person),
            onPressed: () {
              print("Profile clicked");
            },
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.only(left: horizontalSpacing, ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Text("Select your Bar"),
            ],
          )],
        ),
      ),
    );
  }
}

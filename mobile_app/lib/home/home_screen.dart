import 'package:flutter/material.dart';
import 'package:mobile_app/home/widgets/bar_card.dart';
import 'package:mobile_app/objects/bar.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Bar> bars = [];

  @override
  void initState() {
    super.initState();
    _initializeBars();
  }

  void _initializeBars() {
    //todo call api to initialize the bars
    bars = [
      Bar(
          name: "Scouts",
          imageUrl:
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FscoutsLogo.png?alt=media&token=512cb083-e65c-4435-ae27-018d7467473c"),
      Bar(
          name: "Coa",
          imageUrl:
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FcoaLogo.png?alt=media&token=956d9fce-9522-4b27-bdf8-75ec5a80a78e"),
      Bar(
          name: "El Rays",
          imageUrl:
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FelraysLogo.png?alt=media&token=623f67c2-3eda-4b80-884c-d175511511e9"),
      Bar(
          name: "Roxxy",
          imageUrl:
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FroxxyLogo.png?alt=media&token=977221d7-3c5a-4937-a045-c43576c7a265"),
      Bar(
          name: "Brothers",
          imageUrl:
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FbrothersLogo.png?alt=media&token=d4b583ee-2fb5-499a-b3a2-04196ff68f98"),
    ];
  }

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
        padding:
            EdgeInsets.only(left: horizontalSpacing, right: horizontalSpacing),
        child: bars.isEmpty
            ? const Center(child: CircularProgressIndicator())
            : SingleChildScrollView(
                child: Column(
                  children: [
                    for (int i = 0; i < bars.length; i += 2) ...[
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          BarCard(bar: bars[i]),
                          if (i + 1 < bars.length) ...[
                            SizedBox(
                              width: horizontalSpacing,
                            ),
                            BarCard(bar: bars[i + 1]),
                          ]
                        ],
                      ),
                      const SizedBox(height: 10),
                    ]
                  ],
                ),
              ),
      ),
    );
  }
}

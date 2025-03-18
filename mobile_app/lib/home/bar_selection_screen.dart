import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/widgets/bar_card.dart';
import 'package:mobile_app/objects/bar.dart';

class BarSelectionScreen extends StatefulWidget {
  const BarSelectionScreen({super.key});

  @override
  State<BarSelectionScreen> createState() => _BarSelectionScreenState();
}

class _BarSelectionScreenState extends State<BarSelectionScreen> {
  List<Bar> bars = [];
  int? selectedBarIndex;

  @override
  void initState() {
    super.initState();
    initializeBars();
  }

  void initializeBars() {
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

  void selectBar(int i) {
    setState(() {
      if (selectedBarIndex == i) {
        selectedBarIndex = null;
      } else {
        selectedBarIndex = i;
      }
    });
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
          style: AppTextStyles.appBarText(screenHeight, Colors.black),
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
      body: GestureDetector(
        onTap: () {
          setState(() {
            selectedBarIndex = null;
          });
        },
        child: Padding(
          padding: EdgeInsets.only(
              left: horizontalSpacing, right: horizontalSpacing),
          child: bars.isEmpty
              ? const Center(child: CircularProgressIndicator())
              : SingleChildScrollView(
                  physics: const AlwaysScrollableScrollPhysics(),
                  child: Column(
                    children: [
                      SizedBox(
                        height: horizontalSpacing,
                      ),
                      for (int i = 0; i < bars.length; i += 2) ...[
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            GestureDetector(
                              onTap: () => selectBar(i),
                              child: BarCard(
                                bar: bars[i],
                                screenHeight: screenHeight,
                                screenWidth: screenWidth,
                                isSelected: selectedBarIndex == i,
                              ),
                            ),
                            if (i + 1 < bars.length) ...[
                              SizedBox(
                                width: horizontalSpacing * 1.5,
                              ),
                              GestureDetector(
                                onTap: () => selectBar(i + 1),
                                child: BarCard(
                                  bar: bars[i + 1],
                                  screenHeight: screenHeight,
                                  screenWidth: screenWidth,
                                  isSelected: selectedBarIndex == i + 1,
                                ),
                              ),
                            ]
                          ],
                        ),
                        SizedBox(height: horizontalSpacing),
                      ]
                    ],
                  ),
                ),
        ),
      ),
      floatingActionButton: Container(
        height: screenWidth * 0.12,
        width: screenWidth - horizontalSpacing * 2,
        child: ElevatedButton(
            style: ElevatedButton.styleFrom(
                backgroundColor: selectedBarIndex != null
                    ? AppColors.primaryColor
                    : Colors.grey),
            onPressed: () {
              if (selectedBarIndex != null) {
                print("${bars[selectedBarIndex!].name}");
              } else {
                print("No bar selected");
              }
            },
            child: Center(
              child: Text(
                "SELECT BAR",
                style:
                    AppTextStyles.buttonText(screenHeight, AppColors.whiteText),
              ),
            )),
      ),
    );
  }
}

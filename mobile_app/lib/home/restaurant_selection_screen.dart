import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/services/api_services.dart';
import 'package:mobile_app/home/widgets/bar_card.dart';
import 'package:mobile_app/classes/bar.dart';
import 'package:mobile_app/utils/token_manager.dart';

class RestaurantSelectionScreen extends StatefulWidget {
  const RestaurantSelectionScreen({super.key});

  @override
  State<RestaurantSelectionScreen> createState() =>
      _RestaurantSelectionScreenState();
}

class _RestaurantSelectionScreenState extends State<RestaurantSelectionScreen> {
  List<Restaurant> restaurants = [];
  int? selectedRestaurantIndex;
  bool isLoading = true;
  bool errorFetching = false;

  @override
  void initState() {
    super.initState();
    isLoading = true;
    loadSavedRestaurants();
  }

  void loadSavedRestaurants() async {
    setState(() {
      isLoading = true;
      errorFetching = false;
    });

    try {
      final fetchedRestaurants = await fetchCustomerRestaurants();
      setState(() {
        restaurants = fetchedRestaurants;
      });
    } catch (e) {
      print("Error loading restaurants: $e");
      setState(() {
        errorFetching = true;
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void selectRestaurant(int i) {
    //todo go to the menu page for that restaurant
    selectedRestaurantIndex = i;
    Navigator.pushNamed(context, '/home/restaurant_menu',
        arguments: {'restaurant': restaurants[i].name});
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
          'Select a restaurant',
          style: AppTextStyles.appBarText(screenHeight, Colors.black),
        ),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.person),
            onSelected: (value) async {
              if (value == 'logout') {
                // Do logout logic here
                await TokenManager.clearTokens();

                print("Logging out...");
                Navigator.pushReplacementNamed(context, "/");
              }
            },
            itemBuilder: (BuildContext context) => [
              const PopupMenuItem<String>(
                value: 'logout',
                child: Text('Logout'),
              ),
            ],
          ),
        ],
      ),
      body: GestureDetector(
        onTap: () {
          setState(() {
            selectedRestaurantIndex = null;
          });
        },
        child: Padding(
          padding: EdgeInsets.only(
              left: horizontalSpacing, right: horizontalSpacing),
          child: isLoading
              ? const Center(child: CircularProgressIndicator())
              : errorFetching
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text("Failed to load restaurants."),
                          const SizedBox(height: 10),
                          ElevatedButton(
                            onPressed: loadSavedRestaurants,
                            child: const Text("Try Again"),
                          ),
                        ],
                      ),
                    )
                  : SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      child: restaurants.isNotEmpty
                          ? Column(
                              children: [
                                SizedBox(
                                  height: horizontalSpacing,
                                ),
                                for (int i = 0;
                                    i < restaurants.length;
                                    i += 2) ...[
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      GestureDetector(
                                        onTap: () => selectRestaurant(i),
                                        child: BarCard(
                                          bar: restaurants[i],
                                          screenHeight: screenHeight,
                                          screenWidth: screenWidth
                                        ),
                                      ),
                                      if (i + 1 < restaurants.length) ...[
                                        SizedBox(
                                          width: horizontalSpacing * 1.5,
                                        ),
                                        GestureDetector(
                                          onTap: () => selectRestaurant(i + 1),
                                          child: BarCard(
                                            bar: restaurants[i + 1],
                                            screenHeight: screenHeight,
                                            screenWidth: screenWidth,
                                          ),
                                        ),
                                      ]
                                    ],
                                  ),
                                  SizedBox(height: horizontalSpacing),
                                ]
                              ],
                            )
                          : Padding(
                              padding: EdgeInsets.only(
                                  left: horizontalSpacing,
                                  right: horizontalSpacing,
                                  top: verticalSpacing * 10,
                                  bottom: verticalSpacing * 10),
                              child: Center(
                                  child: Text(
                                "You haven't saved any restaurants yet. Click below to add one 🔍",
                                textAlign: TextAlign.center,
                                style: AppTextStyles.subtitleParagraph(
                                    screenHeight, AppColors.paragraphText),
                              ))),
                    ),
        ),
      ),
      // floatingActionButton: !isLoading && !errorFetching ? Container(
      //   height: screenWidth * 0.12,
      //   width: screenWidth - horizontalSpacing * 2,
      //   child: ElevatedButton(
      //       style: ElevatedButton.styleFrom(
      //           backgroundColor: selectedRestaurantIndex != null
      //               ? AppColors.primaryColor
      //               : Colors.grey),
      //       onPressed: () {
      //         if (selectedRestaurantIndex != null) {
      //           print("${restaurants[selectedRestaurantIndex!].name}");
      //         } else {
      //           print("No bar selected");
      //         }
      //       },
      //       child: Center(
      //         child: Text(
      //           "ADD RESTAURANT",
      //           style:
      //               AppTextStyles.buttonText(screenHeight, AppColors.whiteText),
      //         ),
      //       )),
      // )
      // : null,
      floatingActionButton: !isLoading && !errorFetching
          ? Container(
              height: screenWidth * 0.12,
              width: screenWidth - horizontalSpacing * 2,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor,
                ),
                onPressed: () {
                  Navigator.pushNamed(context, "/add_restaurant");
                },
                icon: const Icon(Icons.add),
                label: Text(
                  "ADD NEW",
                  style: AppTextStyles.buttonText(
                      screenHeight, AppColors.whiteText),
                ),
              ),
            )
          : null,
    );
  }
}



    // restaurants = [
    //   Restaurant(
    //       name: "Scouts",
    //       imageUrl:
    //           "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FscoutsLogo.png?alt=media&token=512cb083-e65c-4435-ae27-018d7467473c"),
    //   Restaurant(
    //       name: "Coa",
    //       imageUrl:
    //           "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FcoaLogo.png?alt=media&token=956d9fce-9522-4b27-bdf8-75ec5a80a78e"),
    //   Restaurant(
    //       name: "El Rays",
    //       imageUrl:
    //           "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FelraysLogo.png?alt=media&token=623f67c2-3eda-4b80-884c-d175511511e9"),
    //   Restaurant(
    //       name: "Roxxy",
    //       imageUrl:
    //           "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FroxxyLogo.png?alt=media&token=977221d7-3c5a-4937-a045-c43576c7a265"),
    //   Restaurant(
    //       name: "Brothers",
    //       imageUrl:
    //           "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FbrothersLogo.png?alt=media&token=d4b583ee-2fb5-499a-b3a2-04196ff68f98"),
    // ];
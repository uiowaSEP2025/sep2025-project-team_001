import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/search_box.dart';
import 'package:mobile_app/home/services/api_services.dart';
import 'package:mobile_app/home/widgets/bar_card.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/utils/token_manager.dart';

class RestaurantAdditionScreen extends StatefulWidget {
  const RestaurantAdditionScreen({super.key});

  @override
  State<RestaurantAdditionScreen> createState() =>
      _RestaurantAdditionScreenState();
}

class _RestaurantAdditionScreenState extends State<RestaurantAdditionScreen> {
  List<Restaurant> restaurants = [];
  int? selectedRestaurantIndex;
  bool isLoading = true;
  bool errorFetching = false;
  String searchQuery = '';

  @override
  void initState() {
    super.initState();
    isLoading = true;
    loadRestaurants();
  }

  void loadRestaurants() async {
    setState(() {
      isLoading = true;
      errorFetching = false;
    });

    try {
      final fetchedRestaurants = await fetchRestaurants();
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
    setState(() {
      if (selectedRestaurantIndex == i) {
        selectedRestaurantIndex = null;
      } else {
        selectedRestaurantIndex = i;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return GestureDetector(
      onTap: () {
            FocusManager.instance.primaryFocus?.unfocus();
          },
      child: Scaffold(
        appBar: AppBar(
          title: Text(
            'Select restaurant to add',
            style: AppTextStyles.appBarText(screenHeight, Colors.black),
          ),
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
                            Text(
                              "Failed to load restaurants.",
                              style: AppTextStyles.subtitleParagraph(
                                  screenHeight, AppColors.paragraphText),
                            ),
                            SizedBox(height: verticalSpacing),
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.primaryColor),
                              onPressed: loadRestaurants,
                              child: Text(
                                "Try Again",
                                style: AppTextStyles.buttonText(
                                    screenHeight, Colors.white),
                              ),
                            ),
                          ],
                        ),
                      )
                    : SingleChildScrollView(
                        physics: const AlwaysScrollableScrollPhysics(),
                        child: Column(
                          children: [
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            SearchBox(
                              screenHeight: screenHeight,
                              hintText: "Search restaurants...",
                              onChanged: (value) {
                                setState(() {
                                  searchQuery = value;
                                });
                                print("Searching for: $value");
                              },
                            ),
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            for (int i = 0; i < restaurants.length; i += 2) ...[
                              Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  GestureDetector(
                                    onTap: () => selectRestaurant(i),
                                    child: BarCard(
                                      bar: restaurants[i],
                                      screenHeight: screenHeight,
                                      screenWidth: screenWidth,
                                      
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
                            ],
                            SizedBox(height: screenHeight*0.1*restaurants.length,)
                            
                          ],
                        ),
                      ),
          ),
        ),
      ),
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
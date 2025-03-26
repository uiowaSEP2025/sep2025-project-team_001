import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/widgets/bar_card.dart';
import 'package:mobile_app/classes/bar.dart';
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

  Future<List<Restaurant>> fetchRestaurants() async {
    final accessToken = await TokenManager.getAccessToken();

    if (accessToken == null) {
      throw Exception('Access token not found');
    }

    final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));
    const String endpoint = "${ApiConfig.baseUrl}/restaurants/list";

    try {
      final response = await dio.get(
        endpoint,
        options: Options(
          headers: {
            "Authorization": "Bearer $accessToken",
            "Content-Type": "application/json",
          },
        ),
      );

      final data = response.data as List<dynamic>;
      return data.map((json) => Restaurant.fromJson(json)).toList();
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception("Access token expired or unauthorized");
      }

      print("Fetch restaurants error: ${e.response?.data}");
      throw Exception("Failed to fetch restaurants: ${e.response?.statusCode}");
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

    return Scaffold(
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
                          const Text("Failed to load restaurants."),
                          const SizedBox(height: 10),
                          ElevatedButton(
                            onPressed: loadRestaurants,
                            child: const Text("Try Again"),
                          ),
                        ],
                      ),
                    )
                  : SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      child: Column(
                        children: [
                          SizedBox(
                            height: horizontalSpacing,
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
                                    isSelected: selectedRestaurantIndex == i,
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
                                      isSelected:
                                          selectedRestaurantIndex == i + 1,
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
      floatingActionButton: Container(
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
            style: AppTextStyles.buttonText(screenHeight, AppColors.whiteText),
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
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/main_navigation/orders/services/api_services.dart';
import 'package:mobile_app/main_navigation/orders/services/methods.dart';
import 'package:mobile_app/utils/user_manager.dart';

class OrderReceiptScreen extends StatefulWidget {
  final Order order;
  const OrderReceiptScreen({super.key, required this.order});

  @override
  State<OrderReceiptScreen> createState() => _OrderReceiptScreenState();
}

class _OrderReceiptScreenState extends State<OrderReceiptScreen> {
  String? customerName;
  Restaurant? restaurant;

  @override
  void initState() {
    super.initState();
    getCustomerName();
    fetchRestaurant();
  }

  void getCustomerName() async {
    final name = await UserManager.getName();
    setState(() {
      customerName = name;
    });
  }

  void fetchRestaurant() async {
    final restaurant =
        await getRestaurant(restaurantId: widget.order.restaurantId);
    setState(() {
      this.restaurant = restaurant;
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
          "Order ready!",
          style: AppTextStyles.appBarText(screenHeight, Colors.black),
        ),
      ),
      body: SizedBox(
        width: screenWidth,
        height: screenHeight,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                height: screenHeight * 0.35,
                color: AppColors.greenBackground,
                child: Padding(
                  padding: EdgeInsets.only(
                      left: horizontalSpacing, right: horizontalSpacing),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (restaurant != null)
                        SizedBox(
                          height: verticalSpacing,
                        ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          if (restaurant != null)
                            if (restaurant!.restaurantImageUrl != null)
                              ClipRRect(
                                borderRadius: BorderRadius.circular(12),
                                child: Image.network(
                                  restaurant!.restaurantImageUrl!,
                                  width: screenWidth * 0.35,
                                  height: screenWidth * 0.34,
                                  fit: BoxFit.cover,
                                  errorBuilder: (context, error, stackTrace) {
                                  print("image error: $error");
                                      return Icon(
                                    Icons.broken_image,
                                    size: 40,
                                    color: Colors.grey,
                                  );}
                                ),
                              ),
                          SizedBox(
                            width: horizontalSpacing,
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                "${widget.order.restaurantName}",
                                style: AppTextStyles.bigBoldLetters(
                                    screenHeight * 0.8, Colors.white),
                              ),
                              SizedBox(
                                height: verticalSpacing * 0.5,
                              ),
                              Container(
                                width: screenWidth * 0.5,
                                child: Text(
                                  "You can collect your items now. Enjoy!",
                                  overflow: TextOverflow.visible,
                                  maxLines: 2,
                                  softWrap: true,
                                  style: AppTextStyles.subtitleParagraph(
                                      screenHeight * 1.1, AppColors.whiteText),
                                ),
                              ),
                            ],
                          )
                        ],
                      ),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      SizedBox(
                        height: verticalSpacing / 2,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                            width: screenWidth * 0.90,
                            height: 0.5,
                            color: Colors.white,
                          ),
                        ],
                      ),
                      SizedBox(
                        height: verticalSpacing / 2,
                      ),
                      Text(
                        "$customerName",
                        style: AppTextStyles.bigBoldLetters(
                            screenHeight * 0.7, AppColors.whiteText),
                      ),
                      SizedBox(
                        height: verticalSpacing * 0.5,
                      ),
                      Text(
                        "Order #${widget.order.id}",
                        style: AppTextStyles.subtitleParagraph(
                            screenHeight, Colors.white),
                      ),
                    ],
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(
                    left: horizontalSpacing, right: horizontalSpacing),
                child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(
                        height: verticalSpacing * 0.5,
                      ),
                      Text(
                        "Items: ",
                        style: AppTextStyles.appBarText(
                            screenHeight, Colors.black),
                      ),
                      SizedBox(
                        height: verticalSpacing * 0.5,
                      ),
                      Column(
                        children: widget.order.items.map((item) {
                          return Padding(
                            padding: EdgeInsets.only(bottom: horizontalSpacing),
                            child: Row(
                              children: [
                                Container(
                                  color: AppColors.secondary,
                                  height: 20,
                                  width: 20,
                                  child:
                                      Center(child: Text("${item['quantity']}")),
                                ),
                                SizedBox(width: horizontalSpacing),
                                Text(item['item_name'] ?? '')
                              ],
                            ),
                          );
                        }).toList(),
                      ),
                      SizedBox(
                        height: verticalSpacing * 2,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          Text(
                            "Total: ${widget.order.totalPrice}",
                            style: AppTextStyles.appBarText(
                                screenHeight, Colors.black),
                          ),
                        ],
                      ),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      SizedBox(
                          height: screenWidth * 0.12,
                          width: screenWidth - horizontalSpacing * 2,
                          child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.primaryColor),
                              onPressed: () {
                                generateAndPrintReceipt(
                                    widget.order, customerName, restaurant);
                              },
                              child: Center(
                                child: Text(
                                  "Get Receipt",
                                  style: AppTextStyles.buttonText(
                                      screenHeight, AppColors.whiteText),
                                ),
                              ))),
                    ]),
              )
            ],
          ),
        ),
      ),
    );
  }
}

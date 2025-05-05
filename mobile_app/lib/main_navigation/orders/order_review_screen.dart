import 'package:flutter/material.dart';
import 'package:flutter_rating/flutter_rating.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/main_navigation/orders/services/api_services.dart';
import 'package:mobile_app/main_navigation/orders/services/methods.dart';
import 'package:mobile_app/utils/user_manager.dart';

class OrderReviewScreen extends StatefulWidget {
  final Order order;
  const OrderReviewScreen({super.key, required this.order});

  @override
  State<OrderReviewScreen> createState() => _OrderReviewScreenState();
}

class _OrderReviewScreenState extends State<OrderReviewScreen> {
  late TextEditingController _reviewController;
  late bool needsReview;
  bool isLoading = true;
  bool errorFetching = false;
  late Order order;
  String? customerName;
  Restaurant? restaurant;
  bool isExpanded = false;

  void getCustomerName() async {
    final name = await UserManager.getName();
    setState(() {
      customerName = name;
    });
  }

  @override
  void dispose() {
    _reviewController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _reviewController = TextEditingController();
    needsReview = !widget.order.reviewed;
    loadOrder(widget.order.id);
    getCustomerName();
    fetchRestaurant();
    super.initState();
  }

  void submitReview(int orderId, double rating, String comment) async {

try {
  final returnOrderId = await reviewOrder(orderId: orderId, rating: rating, review: comment);

  if(returnOrderId == order.id){
    ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Review submitted"),
          backgroundColor: AppColors.validGreen,
        ),
      );
    setState(() {
      needsReview = false;
    });
  }
}
catch (e) {
  throw Exception();
}
  }

  void fetchRestaurant() async {
    final restaurant =
        await getRestaurant(restaurantId: widget.order.restaurantId);
    setState(() {
      this.restaurant = restaurant;
    });
  }

  void loadOrder(int orderId) async {
    setState(() {
      isLoading = true;
      errorFetching = false;
    });

    try {
      final fetchedOrder = await getOrder(orderId: orderId);

      setState(() {
        order = fetchedOrder;
      });
    } catch (e) {
      setState(() {
        errorFetching = true;
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
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
          title: Text("Order #${widget.order.id}"),
        ),
        body: isLoading
            ? const Center(child: CircularProgressIndicator())
            : errorFetching
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text("Failed to load order."),
                        const SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: () {
                            loadOrder(widget.order.id);
                          },
                          child: const Text("Try Again"),
                        ),
                      ],
                    ),
                  )
                : Container(
                    width: screenWidth,
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                height: screenHeight * 0.32,
                                color: AppColors.greenBackground,
                                child: Padding(
                                  padding: EdgeInsets.only(
                                      left: horizontalSpacing,
                                      right: horizontalSpacing),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      if (restaurant != null)
                                        SizedBox(
                                          height: verticalSpacing,
                                        ),
                                      Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
                                        children: [
                                          if (restaurant != null)
                                            if (restaurant!
                                                    .restaurantImageUrl !=
                                                null)
                                              ClipRRect(
                                                borderRadius:
                                                    BorderRadius.circular(12),
                                                child: Image.network(
                                                    restaurant!
                                                        .restaurantImageUrl!,
                                                    width: screenWidth * 0.35,
                                                    height: screenWidth * 0.34,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (context,
                                                        error, stackTrace) {
                                                  print("image error: $error");
                                                  return Icon(
                                                    Icons.broken_image,
                                                    size: 40,
                                                    color: Colors.grey,
                                                  );
                                                }),
                                              ),
                                          SizedBox(
                                            width: horizontalSpacing,
                                          ),
                                          Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                "${widget.order.restaurantName}",
                                                style: AppTextStyles
                                                    .bigBoldLetters(
                                                        screenHeight * 0.8,
                                                        Colors.white),
                                              ),
                                              SizedBox(
                                                height: verticalSpacing * 0.5,
                                              ),
                                              Container(
                                                width: screenWidth * 0.5,
                                                child: Text(
                                                  widget.order.status ==
                                                          "completed"
                                                      ? "You can collect your items now. Enjoy!"
                                                      : widget.order
                                                                  .drinkStatus ==
                                                              "completed"
                                                          ? "You can collect your drinks now, your food will be ready shortly!"
                                                          : "You can collect your food now, your drinks will be ready shortly!",
                                                  overflow:
                                                      TextOverflow.visible,
                                                  //maxLines: 2,
                                                  softWrap: true,
                                                  style: AppTextStyles
                                                      .subtitleParagraph(
                                                          screenHeight * 1.1,
                                                          AppColors.whiteText),
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
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
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
                                            screenHeight * 0.7,
                                            AppColors.whiteText),
                                      ),
                                      
                                    ],
                                  ),
                                ),
                              ),
                              SizedBox(
                                height: verticalSpacing,
                              ),
                              Padding(
                                padding: EdgeInsets.only(
                                    left: horizontalSpacing,
                                    right: horizontalSpacing),
                                
                                child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                  children: [
                                    SizedBox(height: verticalSpacing * 0.5),

                                    GestureDetector(
                                      onTap: () {
                                        setState(() {
                                          isExpanded = !isExpanded;
                                        });
                                      },
                                      child: Row(
                                        children: [
                                          Text(
                                            "Items",
                                            style: AppTextStyles.appBarText(
                                                screenHeight, Colors.black),
                                          ),
                                          const SizedBox(width: 5),
                                          Icon(
                                            isExpanded
                                                ? Icons.expand_less
                                                : Icons.expand_more,
                                            size: 20,
                                            color: Colors.black,
                                          )
                                        ],
                                      ),
                                    ),

                                    AnimatedCrossFade(
                                      duration:
                                          const Duration(milliseconds: 200),
                                      crossFadeState: isExpanded
                                          ? CrossFadeState.showSecond
                                          : CrossFadeState.showFirst,
                                      firstChild: const SizedBox.shrink(),
                                      secondChild: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          SizedBox(
                                              height: verticalSpacing * 0.5),

                                          Column(
                                            children: widget.order.items
                                                .map((item) {
                                              return Padding(
                                                padding: EdgeInsets.only(
                                                    bottom:
                                                        horizontalSpacing),
                                                child: Row(
                                                  children: [
                                                    Container(
                                                      color:
                                                          AppColors.secondary,
                                                      height: 20,
                                                      width: 20,
                                                      child: Center(
                                                          child: Text(
                                                              "${item['quantity']}")),
                                                    ),
                                                    SizedBox(
                                                        width:
                                                            horizontalSpacing),
                                                    Text(item['item_name'] ??
                                                        '')
                                                  ],
                                                ),
                                              );
                                            }).toList(),
                                          ),

                                          SizedBox(
                                              height: verticalSpacing * 0.5),

                                          Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.end,
                                            children: [
                                              Text(
                                                "Total: ${widget.order.totalPrice}",
                                                style:
                                                    AppTextStyles.appBarText(
                                                        screenHeight,
                                                        Colors.black),
                                              ),
                                            ],
                                          ),

                                          SizedBox(height: verticalSpacing),

                                          SizedBox(
                                            height: screenWidth * 0.12,
                                            width: screenWidth -
                                                horizontalSpacing * 2,
                                            child: ElevatedButton(
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor:
                                                    AppColors.primaryColor,
                                              ),
                                              onPressed: () {
                                                generateAndPrintReceipt(
                                                    widget.order,
                                                    customerName,
                                                    restaurant);
                                              },
                                              child: Center(
                                                child: Text(
                                                  "Get Receipt",
                                                  style: AppTextStyles
                                                      .buttonText(
                                                          screenHeight,
                                                          AppColors
                                                              .whiteText),
                                                ),
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                )
                              ),
                              SizedBox(height: verticalSpacing,),
                              if (order.status == "picked_up" &&
                                  !order.reviewed && needsReview)
                                RatingWidget(
                                    order: order,
                                    screenHeight: screenHeight,
                                    verticalSpacing: verticalSpacing,
                                    screenWidth: screenWidth,
                                    horizontalSpacing: horizontalSpacing,
                                    reviewController: _reviewController,
                                    onSubmit: submitReview),
                              SizedBox(height: verticalSpacing),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
      ),
    );
  }
}

class RatingWidget extends StatefulWidget {
  const RatingWidget(
      {super.key,
      required this.order,
      required this.screenHeight,
      required this.verticalSpacing,
      required this.screenWidth,
      required this.horizontalSpacing,
      required TextEditingController reviewController,
      required this.onSubmit})
      : _reviewController = reviewController;

  final Order order;
  final double screenHeight;
  final double verticalSpacing;
  final double screenWidth;
  final double horizontalSpacing;
  final TextEditingController _reviewController;
  final void Function(int, double, String) onSubmit;

  @override
  State<RatingWidget> createState() => _RatingWidgetState();
}

class _RatingWidgetState extends State<RatingWidget> {
  double rating = 0;

  void ratingChanged(double rating) {
    setState(() {
      this.rating = rating;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
          SizedBox(width:widget.horizontalSpacing,),
            Text(
              "How was ${widget.order.restaurantName}?",
              style: AppTextStyles.subtitleParagraph(
                  widget.screenHeight * 1.5, AppColors.paragraphText),
            ),
          ],
        ),
        SizedBox(
          height: widget.verticalSpacing,
        ),
        RatingBar.builder(
          itemSize: widget.screenWidth * 0.12,
          initialRating: 0,
          minRating: 1,
          direction: Axis.horizontal,
          allowHalfRating: false,
          itemCount: 5,
          itemPadding: EdgeInsets.symmetric(horizontal: 4.0),
          itemBuilder: (context, _) => const Icon(
            Icons.star,
            color: Colors.amber,
          ),
          onRatingUpdate: (rating) {
            ratingChanged(rating);
          },
        ),
        Padding(
          padding: EdgeInsets.only(
              top: widget.horizontalSpacing,
              bottom: widget.horizontalSpacing,
              left: widget.horizontalSpacing * 2,
              right: widget.horizontalSpacing * 2),
          child: Container(
            padding: EdgeInsets.only(
                top: widget.horizontalSpacing / 4,
                left: widget.horizontalSpacing / 2,
                right: widget.horizontalSpacing / 2,
                bottom: widget.horizontalSpacing / 4),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.grey.shade400),
              borderRadius: BorderRadius.circular(8),
            ),
            child: TextField(
              controller: widget._reviewController,
              minLines: 4,
              maxLines: 6,
              decoration: InputDecoration(
                hintText: "Give ${widget.order.restaurantName} a review...",
                border: InputBorder.none,
              ),
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.only(
              left: widget.horizontalSpacing * 4,
              right: widget.horizontalSpacing * 4),
          child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor),
              onPressed: () {
                widget.onSubmit(
                    widget.order.id, rating, widget._reviewController.text);
              },
              child: Center(
                child: Text(
                  "Post Review",
                  style: AppTextStyles.buttonText(
                      widget.screenHeight, AppColors.whiteText),
                ),
              )),
        ),
      ],
    );
  }
}

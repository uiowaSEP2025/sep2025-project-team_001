import 'package:flutter/material.dart';
import 'package:flutter_rating/flutter_rating.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/main_navigation/orders/services/api_services.dart';

class OrderReceiptScreen extends StatefulWidget {
  Order order;
  OrderReceiptScreen({super.key, required this.order});

  @override
  State<OrderReceiptScreen> createState() => _OrderReceiptScreenState();
}

class _OrderReceiptScreenState extends State<OrderReceiptScreen> {
  late TextEditingController _reviewController;
  late bool needsReview;
  bool isLoading = true;
  bool errorFetching = false;
  late Order order;

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
    super.initState();
  }

  void submitReview(int orderId, double rating, String comment){
    setState(() async {
                  await reviewOrder(
                      orderId: orderId,
                      rating: rating,
                      review: comment);
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
          title: Text(
              "Order: #${widget.order.id} has been reviewed: ${widget.order.reviewed}"),
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
                    child: Column(
                      children: [
                        if (order.status == "picked_up" && !order.reviewed)
                          RatingWidget(
                              order: order,
                              screenHeight: screenHeight,
                              verticalSpacing: verticalSpacing,
                              screenWidth: screenWidth,
                              horizontalSpacing: horizontalSpacing,
                              reviewController: _reviewController,
                              onSubmit: submitReview),
                      ],
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
      required TextEditingController reviewController, required this.onSubmit})
      : _reviewController = reviewController;

  final Order order;
  final double screenHeight;
  final double verticalSpacing;
  final double screenWidth;
  final double horizontalSpacing;
  final TextEditingController _reviewController;
  final void Function(int,double,String) onSubmit;
  

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
        Text(
          "How was ${widget.order.restaurantName}?",
          style: AppTextStyles.subtitleParagraph(
              widget.screenHeight * 1.5, AppColors.paragraphText),
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
              left: widget.horizontalSpacing * 2,
              right: widget.horizontalSpacing * 2),
          child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor),
              onPressed: () {
                widget.onSubmit(widget.order.id, rating, widget._reviewController.text);
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

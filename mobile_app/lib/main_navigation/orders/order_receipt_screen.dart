import 'package:flutter/material.dart';
import 'package:flutter_rating/flutter_rating.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';

class OrderReceiptScreen extends StatefulWidget {
  Order order;
  OrderReceiptScreen({super.key, required this.order});

  @override
  State<OrderReceiptScreen> createState() => _OrderReceiptScreenState();
}

class _OrderReceiptScreenState extends State<OrderReceiptScreen> {
  double rating = 0;

  late TextEditingController _reviewController;

  @override
  void dispose() {
    _reviewController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _reviewController = TextEditingController();
    super.initState();
  }

  void ratingChanged(double rating){
    setState(() {
      this.rating = rating;
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
          title: Text("Order: #${widget.order.id}"),
        ),
        body: Container(
          width: screenWidth,
          child: Column(
            children: [
              if(widget.order.status == "picked_up" && !widget.order.reviewed) RatingWidget(widget: widget, screenHeight: screenHeight, verticalSpacing: verticalSpacing, screenWidth: screenWidth, horizontalSpacing: horizontalSpacing, reviewController: _reviewController, ratingChanged: ratingChanged),
            ],
          ),
       
        ),
      ),
    );
  }
}

class RatingWidget extends StatelessWidget {
  const RatingWidget({
    super.key,
    required this.widget,
    required this.screenHeight,
    required this.verticalSpacing,
    required this.screenWidth,
    required this.horizontalSpacing,
    required TextEditingController reviewController, required this.ratingChanged,
  }) : _reviewController = reviewController;

  final OrderReceiptScreen widget;
  final double screenHeight;
  final double verticalSpacing;
  final double screenWidth;
  final double horizontalSpacing;
  final TextEditingController _reviewController;
  final void Function(double rating) ratingChanged;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          "How was ${widget.order.restaurantName}?",
          style: AppTextStyles.subtitleParagraph(
              screenHeight * 1.5, AppColors.paragraphText),
        ),
        SizedBox(
          height: verticalSpacing,
        ),
        RatingBar.builder(
          itemSize: screenWidth * 0.15,
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
          padding: EdgeInsets.all(horizontalSpacing),
          child: Container(
            padding: EdgeInsets.only(
                top: horizontalSpacing / 4,
                left: horizontalSpacing / 2,
                right: horizontalSpacing / 2,
                bottom: horizontalSpacing / 4),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.grey.shade400),
              borderRadius: BorderRadius.circular(8),
            ),
            child: TextField(
              controller: _reviewController,
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
          padding: EdgeInsets.only(left:horizontalSpacing, right: horizontalSpacing),
          child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor),
              onPressed: (){},
              child: Center(
                      child: Text(
                        "Post Review",
                        style: AppTextStyles.buttonText(
                            screenHeight, AppColors.whiteText),
                      ),
                    )),
        ),
      ],
    );
  }
}

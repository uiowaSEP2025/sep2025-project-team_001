import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/utils/user_manager.dart';

class OrderReceiptScreen extends StatefulWidget {
  final Order order;
  const OrderReceiptScreen({super.key, required this.order});

  @override
  State<OrderReceiptScreen> createState() => _OrderReceiptScreenState();
}

class _OrderReceiptScreenState extends State<OrderReceiptScreen> {
  String? customerName;

  @override
  void initState() {
    super.initState();
    getCustomerName();
  }

  void getCustomerName() async {
    final name = await UserManager.getName();
    setState(() {
      customerName = name;
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
        title: Text("Order ready!", style: AppTextStyles.appBarText(screenHeight, Colors.black),),
      ),
      body: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Padding(
          padding: EdgeInsets.only(
              left: horizontalSpacing, right: horizontalSpacing),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                height: verticalSpacing,
              ),
              Text("You can collect your items now. Enjoy!", style: AppTextStyles.subtitleParagraph(screenHeight, AppColors.paragraphText),),
              Container(
                width: screenWidth * 0.8,
                height: verticalSpacing * 0.5,
              ),
              Text("$customerName"),
              SizedBox(
                height: verticalSpacing,
              ),
              Text("Order #${widget.order.id}"),
            ],
          ),
        ),
      ),
    );
  }
}

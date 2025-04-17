import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/main_navigation/orders/services/methods.dart';

class OrderHistoryScreen extends StatelessWidget {
  final List<Order> pickedUpOrders;

  const OrderHistoryScreen({super.key, required this.pickedUpOrders});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      appBar: AppBar(
          title: Text('Order History',
              style: AppTextStyles.appBarText(screenHeight, Colors.black))),
      body: pickedUpOrders.isEmpty
          ? const Center(child: Text("No past orders yet."))
          : ListView.builder(
              itemCount: pickedUpOrders.length,
              itemBuilder: (context, index) {
                return buildOrderTile(pickedUpOrders[index]);
              },
            ),
    );
  }
}

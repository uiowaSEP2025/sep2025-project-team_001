import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';

class OrderReceiptScreen extends StatelessWidget {
  Order order;
  OrderReceiptScreen({super.key, required this.order});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Order: #${order.id}"),
      ),
    );
  }
}

import 'package:flutter/material.dart';

class OrdersScreen extends StatelessWidget {
  const OrdersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Orders'),
      ),
      body: const Center(
        child: Text(
          "You haven't placed any orders yet.",
          style: TextStyle(fontSize: 16),
        ),
      ),
    );
  }
}

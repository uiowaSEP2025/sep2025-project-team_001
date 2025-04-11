 import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';

Widget buildOrderTile(Order order) {
    return ExpansionTile(
      title: Text("Order #${order.id}"),
      subtitle: Text("Placed on ${order.startTime}"),
      trailing: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text("${getTotalItems(order.items)} items"),
          const SizedBox(height: 4),
          Text(
            "\$${order.totalPrice.toStringAsFixed(2)}",
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ],
      ),
      children: order.items.map((item) {
        return ListTile(
          title: Text(item['item_name'] ?? 'Unnamed item'),
          subtitle: Text("Quantity: ${item['quantity']}"),
          visualDensity: VisualDensity.compact,
        );
      }).toList(),
    );
  }

    int getTotalItems(List<dynamic> items) {
    int total = 0;
    for (var item in items) {
      final quantity = item['quantity'];
      if (quantity is int && quantity > 0) {
        total += quantity;
      } else {
        total += 1;
      }
    }
    return total;
  }
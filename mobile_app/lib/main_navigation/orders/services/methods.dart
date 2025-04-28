import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/main_navigation/orders/services/api_services.dart';
import 'package:mobile_app/main_navigation/orders/widgets/custom_expandable_tile.dart';

Widget buildOrderTile(Order order, double screenHeight, double screenWidth) {
  return CustomExpandableTile(
    screenHeight: screenHeight,
    collapsedChild: Container(
      decoration: BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: EdgeInsets.all(screenHeight * 0.01),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              children: [
                Text("Order #${order.id} for ${order.restaurantName}"),
                SizedBox(height: screenHeight * 0.01),
                Text("${order.items.length} items"),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text("\$${order.totalPrice}"),
                
              ],
            ),
          ],
        ),
      ),
    ),
    expandedChild: Column(
      children: order.items.map((item) {
        return ListTile(
          title: Text(item['item_name'] ?? ''),
          subtitle: Text("Qty: ${item['quantity']}"),
        );
      }).toList(),
    ),
  );

  // return ExpansionTile(
  //   title: Text("Order #${order.id}"),
  //   subtitle: Text("Placed on ${order.startTime}"),
  //   trailing: Column(
  //     crossAxisAlignment: CrossAxisAlignment.end,
  //     children: [
  //       Text("${getTotalItems(order.items)} items"),
  //       const SizedBox(height: 4),
  //       Text(
  //         "\$${order.totalPrice.toStringAsFixed(2)}",
  //         style: const TextStyle(fontWeight: FontWeight.bold),
  //       ),
  //     ],
  //   ),
  //   children: order.items.map((item) {
  //     return ListTile(
  //       title: Text(item['item_name'] ?? 'Unnamed item'),
  //       subtitle: Text("Quantity: ${item['quantity']}"),
  //       visualDensity: VisualDensity.compact,
  //     );
  //   }).toList(),
  // );

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

Widget buildPendingOrderTile(
    Order order, double screenHeight, double screenWidth) {
  return CustomExpandableTile(
    screenHeight: screenHeight,
    collapsedChild: Container(
      decoration: BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: EdgeInsets.all(screenHeight * 0.01),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              children: [
                Text("Order #${order.id} for ${order.restaurantName}"),
                SizedBox(height: screenHeight * 0.01),
                Text("${order.items.length} items"),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text("\$${order.totalPrice}"),
                TextButton(
                  onPressed: () => cancelOrder(
                      orderId: order.id, restaurantId: order.restaurantId),
                  style: TextButton.styleFrom(foregroundColor: Colors.red),
                  child: const Text("Cancel"),
                ),
              ],
            ),
          ],
        ),
      ),
    ),
    expandedChild: Column(
      children: order.items.map((item) {
        return ListTile(
          title: Text(item['item_name'] ?? ''),
          subtitle: Text("Qty: ${item['quantity']}"),
        );
      }).toList(),
    ),
  );

}

import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/main_navigation/orders/order_receipt_screen.dart';
import 'package:mobile_app/main_navigation/orders/order_review_screen.dart';
import 'package:mobile_app/main_navigation/orders/services/api_services.dart';
import 'package:mobile_app/main_navigation/orders/widgets/custom_expandable_tile.dart';

Widget buildHistoryOrderTile(BuildContext context, Order order,
    double screenHeight, double screenWidth) {
  return GestureDetector(
    onTap: () {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => OrderReviewScreen(order: order)),
      );
    },
    child: Container(
      decoration: BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: EdgeInsets.all(screenHeight * 0.02),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Order #${order.id} for ${order.restaurantName}",
                  style: AppTextStyles.buttonText(
                      screenHeight * 0.9, Colors.black),
                ),
                SizedBox(height: screenHeight * 0.01),
                Text("${order.items.length} items"),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text("\$${order.totalPrice}",
                    style: AppTextStyles.buttonText(
                        screenHeight * 0.8, Colors.black)),
                SizedBox(height: screenWidth * 0.03),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => OrderReviewScreen(order: order)),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    textStyle: AppTextStyles.buttonText(
                        screenHeight * 0.7, AppColors.whiteText),
                  ),
                  child: const Text("View Details"),
                )
              ],
            ),
          ],
        ),
      ),
    ),
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
    expandedChild: Padding(
      padding: EdgeInsets.only(
          left: screenWidth * 0.015, right: screenWidth * 0.015),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(10),
              bottomRight: Radius.circular(10)),
          color: AppColors.secondary.withOpacity(0.4),
        ),
        child: Column(
          children: order.items.map((item) {
            return ListTile(
              title: Text(item['item_name'] ?? ''),
              subtitle: Text("Qty: ${item['quantity']}"),
            );
          }).toList(),
        ),
      ),
    ),
  );
}

Widget buildProgressOrderTile( BuildContext context,
    Order order, double screenHeight, double screenWidth) {
  return CustomExpandableTile(
    screenHeight: screenHeight,
    collapsedChild: Container(
      decoration: BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: EdgeInsets.all(screenHeight * 0.02),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Order #${order.id} for ${order.restaurantName}",
                  style: AppTextStyles.buttonText(
                      screenHeight * 0.9, Colors.black),
                ),
                SizedBox(height: screenHeight * 0.01),
                if (order.drinksETAminutes != null &&
                    order.drinkStatus != 'completed')
                  Text("Drinks ready in ${order.drinksETAminutes} minutes"),
                if (order.drinkStatus == 'completed')
                  ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => OrderReceiptScreen(order: order)),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    textStyle: AppTextStyles.buttonText(
                        screenHeight * 0.7, AppColors.whiteText),
                  ),
                  child: const Text("Pick up Drinks Now!"),
                ),
                  // Text(
                  //   "Pick up Drinks now!",
                  //   style: AppTextStyles.buttonText(
                  //       screenHeight, AppColors.primaryColor),
                  // ),
                SizedBox(height: screenHeight * 0.01),
                if (order.foodETAminutes != null &&
                    order.foodStatus != 'completed')
                  Text(
                      "Food will be ready in ${order.drinksETAminutes} minutes"),
                if (order.foodStatus == 'completed')
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => OrderReceiptScreen(order: order)),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    textStyle: AppTextStyles.buttonText(
                        screenHeight * 0.7, AppColors.whiteText),
                  ),
                  child: const Text("Pick up Food Now!"),
                ),
                  // Text(
                  //     "Pick up Food now!",
                  //     style: AppTextStyles.buttonText(
                  //         screenHeight, AppColors.primaryColor),
                  //   ),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text("\$${order.totalPrice}",
                    style: AppTextStyles.buttonText(
                        screenHeight * 0.8, Colors.black)),
                SizedBox(height: screenHeight * 0.01),
                Text("${order.items.length} items"),
              ],
            ),
          ],
        ),
      ),
    ),
    expandedChild: Padding(
      padding: EdgeInsets.only(
          left: screenWidth * 0.015, right: screenWidth * 0.015),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(10),
              bottomRight: Radius.circular(10)),
          color: AppColors.secondary.withOpacity(0.4),
        ),
        child: Column(
          children: order.items.map((item) {
            return ListTile(
              title: Text(item['item_name'] ?? ''),
              subtitle: Text("Qty: ${item['quantity']}"),
            );
          }).toList(),
        ),
      ),
    ),
  );
}

Widget buildPickupOrderTile(BuildContext context, Order order,
    double screenHeight, double screenWidth) {
  return GestureDetector(
    onTap: () {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => OrderReceiptScreen(order: order)),
      );
    },
    child: Container(
      decoration: BoxDecoration(
        color: AppColors.secondary,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: EdgeInsets.all(screenHeight * 0.02),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Order #${order.id} for ${order.restaurantName}",
                  style: AppTextStyles.buttonText(
                      screenHeight * 0.9, Colors.black),
                ),
                SizedBox(height: screenHeight * 0.01),
                Text("${order.items.length} items"),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text("\$${order.totalPrice}",
                    style: AppTextStyles.buttonText(
                        screenHeight * 0.8, Colors.black)),
                SizedBox(height: screenWidth * 0.03),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => OrderReceiptScreen(order: order)),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    textStyle: AppTextStyles.buttonText(
                        screenHeight * 0.7, AppColors.whiteText),
                  ),
                  child: const Text("Pick up Now"),
                )
              ],
            ),
          ],
        ),
      ),
    ),
  );
}

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/services/api_services.dart';
import 'package:mobile_app/main_navigation/orders/services/methods.dart';
import 'package:mobile_app/utils/user_manager.dart';

class OrdersScreen extends StatefulWidget {
  const OrdersScreen({super.key});

  @override
  State<OrdersScreen> createState() => _OrdersScreenState();
}

class _OrdersScreenState extends State<OrdersScreen> {
  bool _initialLoadDone = false;

  Timer? _pollingTimer;
  List<Order> orders = [];
  bool isLoading = true;
  bool errorFetching = false;
  List<Order> pendingOrders = [];
  List<Order> completedOrders = [];
  List<Order> inProgressOrders = [];
  List<Order> pickedUpOrders = [];

  @override
  void initState() {
    super.initState();
    _loadOrders();
    _startPolling();
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  void _startPolling() {
    _pollingTimer = Timer.periodic(const Duration(seconds: 5), (timer) {
      _loadOrders();
    });
  }

  Future<void> _loadOrders() async {
    if (!_initialLoadDone) {
      setState(() {
        isLoading = true;
        errorFetching = false;
      });
    }

    try {
      final userId = await UserManager.getUser();
      if (userId == null) throw Exception("Customer ID not found");

      final fetchedOrders = await fetchUserOrders(userId);

      final newPending =
          fetchedOrders.where((o) => o.status == 'pending').toList();
      final newCompleted =
          fetchedOrders.where((o) => o.status == 'completed').toList();
      final newInProgress =
          fetchedOrders.where((o) => o.status == 'in_progress').toList();
      final newPickedUp =
          fetchedOrders.where((o) => o.status == 'picked_up').toList();

      if (!_listEquals(pendingOrders, newPending) ||
          !_listEquals(completedOrders, newCompleted) ||
          !_listEquals(inProgressOrders, newInProgress) ||
          !_listEquals(pickedUpOrders, newPickedUp)) {
        setState(() {
          pendingOrders = newPending;
          completedOrders = newCompleted;
          inProgressOrders = newInProgress;
          pickedUpOrders = newPickedUp;
        });
      }
    } catch (e) {
      print("Error loading orders: $e");
      if (!_initialLoadDone) {
        setState(() => errorFetching = true);
      }
    } finally {
      if (!_initialLoadDone) {
        setState(() {
          isLoading = false;
          _initialLoadDone = true;
        });
      }
    }
  }

  bool _listEquals(List<Order> a, List<Order> b) {
    if (a.length != b.length) return false;
    for (int i = 0; i < a.length; i++) {
      if (a[i].id != b[i].id ||
          a[i].status != b[i].status ||
          a[i].items.length != b[i].items.length) {
        return false;
      }
    }
    return true;
  }

  Widget buildPendingOrderTile(Order order, double screenHeight) {
    return ExpansionTile(
      title: Container(height: 200, child: Text("Order #${order.id}")),
      subtitle: Text("Placed on ${order.startTime}"),
      trailing: Container(
        height: 600,
        color: AppColors.primaryColor,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text("${getTotalItems(order.items)} items"),
             SizedBox(height: screenHeight*0.015),
            Text(
              "\$${order.totalPrice.toStringAsFixed(2)}",
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            TextButton(
              onPressed: () {},
              style: TextButton.styleFrom(foregroundColor: Colors.red),
              child: const Text("Cancel"),
            ),
          ],
        ),
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

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
      appBar: AppBar(
          title: Text(
            'Your Orders',
            style: AppTextStyles.appBarText(screenHeight, Colors.black),
          ),
          actions: [
            IconButton(
              icon: const Icon(Icons.history),
              tooltip: 'Order History',
              onPressed: () {
                Navigator.pushNamed(context, '/orders/order_history',
                    arguments: {'orders': pickedUpOrders});
              },
            ),
          ]),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorFetching
              ? const Center(child: Text('Failed to load orders. Try again.'))
              : (pendingOrders.isEmpty && completedOrders.isEmpty)
                  ? const Center(
                      child: Text("You haven't placed any orders yet."))
                  : ListView(
                      children: [
                        if (pendingOrders.isNotEmpty) ...[
                           Padding(
                            padding: EdgeInsets.all(verticalSpacing),
                            child: Text("Pending Orders",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                          ...pendingOrders
                              .map((order) => buildPendingOrderTile(order, screenHeight)),
                        ],
                        if (completedOrders.isNotEmpty) ...[
                           Padding(
                            padding: EdgeInsets.all(verticalSpacing),
                            child: Text("Completed",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                          ...completedOrders
                              .map((order) => buildOrderTile(order)),
                        ],
                        if (inProgressOrders.isNotEmpty) ...[
                           Padding(
                            padding: EdgeInsets.all(verticalSpacing),
                            child: Text("In Progress",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                          ...inProgressOrders
                              .map((order) => buildOrderTile(order)),
                        ],
                      ],
                    ),
    );
  }
}

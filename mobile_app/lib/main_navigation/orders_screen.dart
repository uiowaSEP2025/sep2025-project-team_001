import 'dart:async';

import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/services/api_services.dart';
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
    _pollingTimer = Timer.periodic(Duration(seconds: 10), (timer) {
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
          fetchedOrders.where((o) => o.status != 'completed').toList();
      final newCompleted =
          fetchedOrders.where((o) => o.status == 'completed').toList();

      if (!_listEquals(pendingOrders, newPending) ||
          !_listEquals(completedOrders, newCompleted)) {
        setState(() {
          pendingOrders = newPending;
          completedOrders = newCompleted;
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

  // Widget _buildOrderTile(Order order) {
  //   return ListTile(
  //     title: Text("Order #${order.id}"),
  //     //subtitle: Text("Placed on ${order.startTime}"),
  //     trailing: Text("${order.items.length} items"),
  //   );
  // }

Widget _buildOrderTile(Order order) {
  return ExpansionTile(
    title: Text("Order #${order.id}"),
    subtitle: Text("Placed on ${order.startTime}"),
trailing: Text("${_getTotalItems(order.items)} items"),
    children: order.items.map((item) {
  return ListTile(
    title: Text(item['item_name'] ?? 'Unnamed item'),
    subtitle: Text("Quantity: ${item['quantity']}"),
    visualDensity: VisualDensity.compact,
  );
}).toList(),

  );
}

int _getTotalItems(List<dynamic> items) {
  int total = 0;
  for (var item in items) {
    final quantity = item['quantity'];
    if (quantity is int && quantity > 0) {
      total += quantity;
    } else {
      total += 1; // fallback if quantity is null or invalid
    }
  }
  return total;
}



  @override
  Widget build(BuildContext context) {
            double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
      appBar: AppBar(title: Text('Your Orders',style: AppTextStyles.appBarText(screenHeight, Colors.black))),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorFetching
              ? Center(child: Text('Failed to load orders. Try again.'))
              : (pendingOrders.isEmpty && completedOrders.isEmpty)
                  ? const Center(
                      child: Text("You haven't placed any orders yet."))
                  : ListView(
                      children: [
                        if (pendingOrders.isNotEmpty) ...[
                           Padding(
                            padding: EdgeInsets.all(8),
                            child: Text("Pending Orders",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                          ...pendingOrders
                              .map((order) => _buildOrderTile(order)),
                        ],
                        if (completedOrders.isNotEmpty) ...[
                          const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Text("Completed Orders",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                          ...completedOrders
                              .map((order) => _buildOrderTile(order)),
                        ]
                      ],
                    ),
    );
  }
}

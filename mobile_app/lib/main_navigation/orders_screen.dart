import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/services/api_services.dart';
import 'package:mobile_app/utils/user_manager.dart';

class OrdersScreen extends StatefulWidget {
  const OrdersScreen({super.key});

  @override
  State<OrdersScreen> createState() => _OrdersScreenState();
}

class _OrdersScreenState extends State<OrdersScreen> {
  List<Order> orders = [];
  bool isLoading = true;
  bool errorFetching = false;

  @override
  void initState() {
    super.initState();
    _loadOrders();
  }

  Future<void> _loadOrders() async {
    setState(() {
      isLoading = true;
      errorFetching = false;
    });

    try {
      final userId = await UserManager.getUser(); // Assuming this returns customer ID
      if (userId == null) throw Exception("Customer ID not found");

      final fetchedOrders = await fetchUserOrders(userId);
      setState(() {
        orders = fetchedOrders;
      });
    } catch (e) {
      print("Error loading orders: $e");
      setState(() => errorFetching = true);
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your Orders')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorFetching
              ? Center(child: Text('Failed to load orders. Try again.'))
              : orders.isEmpty
                  ? const Center(child: Text("You haven't placed any orders yet."))
                  : ListView.builder(
                      itemCount: orders.length,
                      itemBuilder: (context, index) {
                        final order = orders[index];
                        return ListTile(
                          title: Text("Order #${order.id}"),
                          subtitle: Text("Placed on ${order.startTime}"),
                          trailing: Text("${order.items.length} items"),
                        );
                      },
                    ),
    );
  }
}

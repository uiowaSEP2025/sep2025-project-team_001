import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/services/api_services.dart';
import 'package:mobile_app/utils/user_manager.dart';

class CartScreen extends StatefulWidget {
  final Map<String, CartItem> cart;
  final Restaurant restaurant;
  final void Function(Map<String, CartItem>) onCartUpdated;

  const CartScreen(
      {super.key,
      required this.cart,
      required this.restaurant,
      required this.onCartUpdated});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  late Map<String, CartItem> _cart;

  @override
  void initState() {
    super.initState();
    _cart = Map.from(widget.cart);
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    void submitOrder() async {
      final customerId = await UserManager.getUser();
      final restaurantId = widget.restaurant.id;

      if (customerId == null) {
        throw Exception('customer id not found');
      }

      try {
        final orderId = await placeOrder(
            customerId: customerId,
            restaurantId: restaurantId,
            cart: widget.cart);

        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("order placed with id $orderId")));
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Error placing order, please try again")));
      }
    }

    double total = _cart.values.fold<double>(
        0, (sum, cartItem) => sum + cartItem.item.price * cartItem.quantity);

    return PopScope(
      canPop: true,
      onPopInvoked: (didPop) {
        if (didPop) {
          widget.onCartUpdated.call(_cart);
        }
      },
      child: Scaffold(
        appBar: AppBar(title: Text('Your Cart')),
        body: ListView(
          children: _cart.entries.map((entry) {
            final key = entry.key;
            final cartItem = entry.value;

            return ListTile(
              title: Text(cartItem.item.name),
              subtitle: Row(
                children: [
                  IconButton(
                    icon: Icon(Icons.remove),
                    onPressed: () {
                      if (cartItem.quantity > 1) {
                        setState(() {
                          _cart[key] = CartItem(
                            item: cartItem.item,
                            quantity: cartItem.quantity - 1,
                          );
                        });
                      }
                    },
                  ),
                  Text('${cartItem.quantity}'),
                  IconButton(
                    icon: Icon(Icons.add),
                    onPressed: () {
                      setState(() {
                        _cart[key] = CartItem(
                          item: cartItem.item,
                          quantity: cartItem.quantity + 1,
                        );
                      });
                    },
                  ),
                ],
              ),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '\$${(cartItem.item.price * cartItem.quantity).toStringAsFixed(2)}',
                  ),
                  IconButton(
                    icon: Icon(Icons.delete, color: Colors.red),
                    onPressed: () {
                      setState(() {
                        _cart.remove(key);
                      });
                    },
                  ),
                ],
              ),
            );
          }).toList(),
        ),
        bottomNavigationBar: Padding(
          padding: EdgeInsets.only(
              left: horizontalSpacing,
              right: horizontalSpacing,
              bottom: verticalSpacing * 2),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Total: \$${total.toStringAsFixed(2)}',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () {
                        widget.onCartUpdated.call(_cart);
                        Navigator.pop(context);
                      },
                      child: Text('Back to Menu'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () {
                        print(widget.restaurant.id);
                        submitOrder();
                      },
                      child: Text('Checkout'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class CartNavigatorObserver extends NavigatorObserver {
  final VoidCallback onPop;

  CartNavigatorObserver({required this.onPop});

  @override
  void didPop(Route route, Route? previousRoute) {
    onPop();
    super.didPop(route, previousRoute);
  }
}

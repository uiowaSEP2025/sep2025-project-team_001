import 'package:flutter/material.dart';
import 'package:mobile_app/classes/menu_item.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';

class CartScreen extends StatelessWidget {
  final Map<String, CartItem> cart;

  const CartScreen({super.key, required this.cart});

  @override
  Widget build(BuildContext context) {
    final total = cart.values.fold<double>(
        0, (sum, cartItem) => sum + cartItem.item.price * cartItem.quantity);

    return Scaffold(
      appBar: AppBar(title: Text('Your Cart')),
      body: ListView(
        children: cart.values.map((cartItem) {
          return ListTile(
            title: Text(cartItem.item.name),
            subtitle: Text('Quantity: ${cartItem.quantity}'),
            trailing: Text('\$${(cartItem.item.price * cartItem.quantity).toStringAsFixed(2)}'),
          );
        }).toList(),
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
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
                    onPressed: () => Navigator.pop(context),
                    child: Text('Back to Menu'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      // Handle checkout
                    },
                    child: Text('Checkout'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

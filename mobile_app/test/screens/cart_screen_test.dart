import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/screens/cart_screen.dart';

void main() {
  late Map<String, CartItem> cart;
  late Restaurant restaurant;
  late void Function(Map<String, CartItem>) onCartUpdated;
  bool onCartUpdatedCalled = false;

  setUp(() {
    cart = {
      'item1': CartItem(item: MenuItem(id: '1', name: 'Delicious Burger', price: 12.50), quantity: 2),
      'item2': CartItem(item: MenuItem(id: '2', name: 'Fries', price: 4.00), quantity: 1),
      'item3': CartItem(item: MenuItem(id: '3', name: 'Soda', price: 2.00), quantity: 3),
    };
    restaurant = Restaurant(id: 1, name: 'Tasty Bites');
    onCartUpdatedCalled = false;
    onCartUpdated = (updatedCart) {
      onCartUpdatedCalled = true;
    };
  });

  Widget makeTestableWidget({required Widget child}) {
    return MaterialApp(
      home: child,
    );
  }

  group('CartScreen UI Tests', () {
    testWidgets('renders the app bar with correct title', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      expect(find.widget<AppBar>(find.byType<AppBar>()), findsOneWidget);
      expect(find.text('Your Cart'), findsOneWidget);
    });

    testWidgets('renders all cart items with correct details', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      expect(find.text('Delicious Burger'), findsOneWidget);
      expect(find.text('Fries'), findsOneWidget);
      expect(find.text('Soda'), findsOneWidget);

      expect(find.text('2'), findsNWidgets(1)); // Quantity of Burger
      expect(find.text('1'), findsNWidgets(1)); // Quantity of Fries
      expect(find.text('3'), findsNWidgets(1)); // Quantity of Soda

      expect(find.text('\$25.00'), findsNWidgets(1)); // Price of Burger (12.50 * 2)
      expect(find.text('\$4.00'), findsNWidgets(1));  // Price of Fries (4.00 * 1)
      expect(find.text('\$6.00'), findsNWidgets(1));  // Price of Soda (2.00 * 3)
    });

    testWidgets('displays the correct initial total price', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      // Total should be (12.50 * 2) + (4.00 * 1) + (2.00 * 3) = 25.00 + 4.00 + 6.00 = 35.00
      expect(find.text('Total: \$35.00'), findsOneWidget);
    });

    testWidgets('increments item quantity and updates total price', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      // Increment Burger quantity
      await tester.tap(find.descendant(of: find.widget(ListTile(title: Text('Delicious Burger'))), matching: find.byIcon(Icons.add)));
      await tester.pumpAndSettle();

      expect(find.text('3'), findsNWidgets(1)); // Updated Burger quantity
      expect(find.text('Total: \$47.50'), findsOneWidget); // Updated total (37.50 + 4.00 + 6.00)
    });

    testWidgets('decrements item quantity and updates total price', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      // Decrement Burger quantity
      await tester.tap(find.descendant(of: find.widget(ListTile(title: Text('Delicious Burger'))), matching: find.byIcon(Icons.remove)));
      await tester.pumpAndSettle();

      expect(find.text('1'), findsNWidgets(1)); // Updated Burger quantity
      expect(find.text('Total: \$26.50'), findsOneWidget); // Updated total (12.50 + 4.00 + 6.00)
    });

    testWidgets('removes item from cart and updates total price', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      // Remove Fries
      await tester.tap(find.descendant(of: find.widget(ListTile(title: Text('Fries'))), matching: find.byIcon(Icons.delete)));
      await tester.pumpAndSettle();

      expect(find.text('Fries'), findsNothing);
      expect(find.text('\$4.00'), findsNothing);
      expect(find.text('Total: \$31.00'), findsOneWidget); // Updated total (25.00 + 6.00)
    });

    testWidgets('renders "Back to Menu" and "Checkout" buttons', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      expect(find.text('Back to Menu'), findsOneWidget);
      expect(find.text('Checkout'), findsOneWidget);
    });

    testWidgets('taps "Back to Menu" button and calls onCartUpdated', (WidgetTester tester) async {
      await tester.pumpWidget(makeTestableWidget(
          child: CartScreen(cart: cart, restaurant: restaurant, onCartUpdated: onCartUpdated)));

      await tester.tap(find.text('Back to Menu'));
      await tester.pumpAndSettle();

      expect(onCartUpdatedCalled, isTrue);
    });

    // Note: We are skipping testing the "Checkout" button's functionality
    // as it involves the ApiServices, which we are choosing not to mock in this scenario.
  });
}
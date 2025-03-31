import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';
import 'package:mobile_app/home/restaurant/widgets/menu_item_card.dart';

void main() {
  final testItemAvailable = MenuItem(
    id: 3,
    category: 'food',
    name: 'Burger',
    description: 'Juicy grilled burger with cheese',
    price: 9.99,
    available: true,
    base64image: '', // fallback should still be triggered
  );

  final testItemUnavailable = MenuItem(
    id: 2,
    category: 'food',
    name: 'Pizza',
    description: 'Delicious cheesy pizza slice',
    price: 12.49,
    available: false,
    base64image: '', // fallback should still be triggered
  );

  const double testScreenHeight = 800;
  const double testScreenWidth = 400;
  const double hSpacing = 16;
  const double vSpacing = 16;

  testWidgets('Renders MenuItemCard with available item and triggers onAddToCart',
      (WidgetTester tester) async {
    MenuItem? tappedItem;

    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: MenuItemCard(
          item: testItemAvailable,
          screenHeight: testScreenHeight,
          screenWidth: testScreenWidth,
          horizontalSpacing: hSpacing,
          verticalSpacing: vSpacing,
          onAddToCart: (item) {
            tappedItem = item;
          },
        ),
      ),
    ));

    // Check image fallback exists
    expect(find.byType(Image), findsWidgets);

    // Check name, description and price
    expect(find.text('Burger'), findsOneWidget);
    expect(find.textContaining('Juicy grilled burger'), findsOneWidget);
    expect(find.text('\$9.99'), findsOneWidget);

    // Check Add to Cart button exists and works
    expect(find.text('Add to Cart'), findsOneWidget);
    await tester.tap(find.text('Add to Cart'));
    await tester.pump();

    expect(tappedItem?.name, equals('Burger'));
  });

  testWidgets('Renders MenuItemCard with unavailable item and no Add button',
      (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: MenuItemCard(
          item: testItemUnavailable,
          screenHeight: testScreenHeight,
          screenWidth: testScreenWidth,
          horizontalSpacing: hSpacing,
          verticalSpacing: vSpacing,
          onAddToCart: (_) {},
        ),
      ),
    ));

    expect(find.text('Pizza'), findsOneWidget);
    expect(find.text('Unavailable'), findsOneWidget);
    expect(find.text('Add to Cart'), findsNothing);
  });

  testWidgets('Handles long descriptions with ellipsis overflow',
      (WidgetTester tester) async {
    final longItem = MenuItem(
      name: 'Wrap',
      description: 'This is a very long description that should be cut off after two lines of text...',
      price: 7.25,
      available: true,
      base64image: '', id: 1, category: 'drink',
    );

    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: MenuItemCard(
          item: longItem,
          screenHeight: testScreenHeight,
          screenWidth: testScreenWidth,
          horizontalSpacing: hSpacing,
          verticalSpacing: vSpacing,
          onAddToCart: (_) {},
        ),
      ),
    ));

    final descText = find.textContaining('This is a very long description');
    expect(descText, findsOneWidget);
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/home_screen.dart';

void main() {
  testWidgets('HomePage UI elements and interactions', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: HomePage(),
      ),
    );

    expect(find.text('Select a bar'), findsOneWidget);

    expect(find.byIcon(Icons.person), findsOneWidget);

    expect(find.text('Select your Bar'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.person));
    await tester.pump();
    
  });
}

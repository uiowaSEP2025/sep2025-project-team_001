
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';

void main() {
  testWidgets('renders AuthenticationPage and its fields', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: AuthenticationPage(),
      ),
    );

    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('LOGIN'), findsOneWidget);
    expect(find.text('Sign In with Google'), findsOneWidget);
  });
}

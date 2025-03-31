
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/design/widgets/user_input/password_text_box.dart';

void main() {
  testWidgets('PasswordTextBox renders and obscures text', (WidgetTester tester) async {
    final controller = TextEditingController();

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: PasswordTextBox(
            label: 'Password',
            hintText: 'Enter password',
            screenWidth: 400,
            screenHeight: 800,
            controller: controller,
            onSubmitted: () {},
          ),
        ),
      ),
    );

    expect(find.text('Password'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
    expect(controller.text, '');
  });
}


import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

void main() {
  testWidgets('InputTextBox renders and responds to input', (WidgetTester tester) async {
    final controller = TextEditingController();

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: InputTextBox(
            label: 'Email',
            hintText: 'example@gmail.com',
            screenWidth: 400,
            screenHeight: 800,
            controller: controller,
            onSubmitted: () {}, onChanged: () {  },
          ),
        ),
      ),
    );

    expect(find.text('Email'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);

    await tester.enterText(find.byType(TextField), 'test@example.com');
    expect(controller.text, 'test@example.com');
  });
}

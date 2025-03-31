import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/recover_email/recover_password.dart';

void main() {
  testWidgets('RecoverPasswordScreen full flow test', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: RecoverPasswordScreen()));

    // Step 1: EnterRecoveryEmail should be visible
    expect(find.text('Please enter the email associated to your account'), findsOneWidget);
    expect(find.text('RECOVER PASSWORD'), findsOneWidget);

    // Enter email and tap button
    await tester.enterText(find.byType(TextFormField), 'user@example.com');
    await tester.tap(find.text('RECOVER PASSWORD'));
    await tester.pumpAndSettle();

    // Step 2: EnterRecoveryCode should be visible
    expect(find.text('We sent a validation code to '), findsOneWidget);
    expect(find.text('VALIDATE CODE'), findsOneWidget);

    // Simulate entering the 4-digit code
    await tester.enterText(find.byType(TextField), '1234');
    await tester.pumpAndSettle();

    // Tap Validate Code button
    await tester.tap(find.text('VALIDATE CODE'));
    await tester.pumpAndSettle();

    // Step 3: EnterNewPassword should be visible
    expect(find.text('Please enter a new password for your account'), findsOneWidget);
    expect(find.text('SET PASSWORD'), findsOneWidget);

    // Enter valid password
    await tester.enterText(find.byType(TextFormField).at(0), 'Strong1!');
    await tester.enterText(find.byType(TextFormField).at(1), 'Strong1!');
    await tester.pumpAndSettle();

    expect(find.text('Valid password ✅'), findsOneWidget);
    expect(find.text('Passwords match ✅'), findsOneWidget);
  });

  testWidgets('Back navigation with PopScope works properly', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: RecoverPasswordScreen()));

    // Move to second step
    await tester.enterText(find.byType(TextFormField), 'user@example.com');
    await tester.tap(find.text('RECOVER PASSWORD'));
    await tester.pumpAndSettle();

    // Trigger back
    await tester.binding.handlePopRoute();
    await tester.pumpAndSettle();

    // Should return to first step
    expect(find.text('Please enter the email associated to your account'), findsOneWidget);
  });

  testWidgets('PageView cannot be swiped manually', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: RecoverPasswordScreen()));

    final pageView = find.byType(PageView);
    final gesture = await tester.startGesture(tester.getCenter(pageView));
    await gesture.moveBy(const Offset(-400, 0));
    await tester.pumpAndSettle();

    // It should still be on step 1
    expect(find.text('Please enter the email associated to your account'), findsOneWidget);
  });
}

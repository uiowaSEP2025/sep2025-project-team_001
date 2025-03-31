import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_new_password.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_recovery_code.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_recovery_email.dart';
import 'package:mobile_app/design/widgets/user_input/four_digit_code_field.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  // Test for EnterNewPassword widget
  testWidgets('EnterNewPassword - renders and validates password fields', (WidgetTester tester) async {
    bool onNextCalled = false;
    await tester.pumpWidget(MaterialApp(
      home: EnterNewPassword(
        enteredEmail: 'test@example.com',
        onNext: () {
          onNextCalled = true;
        },
      ),
    ));

    expect(find.text("Please enter a new password for your account"), findsOneWidget);
    expect(find.byType(TextFormField), findsNWidgets(2));  // Two password fields

    final passwordField = find.byType(TextFormField).at(0);  // New password field
    final confirmField = find.byType(TextFormField).at(1);   // Confirm password field

    await tester.enterText(passwordField, 'Password123!');
    await tester.enterText(confirmField, 'Password123!');
    await tester.pumpAndSettle();

    expect(find.text('Valid password ✅'), findsOneWidget);
    expect(find.text('Passwords match ✅'), findsOneWidget);

    final submitButton = find.widgetWithText(ElevatedButton, 'SET PASSWORD');
    await tester.tap(submitButton);
    await tester.pumpAndSettle();

    expect(onNextCalled, false);  // onNext should not be called without API implementation

    await tester.enterText(passwordField, 'Password123');
    await tester.enterText(confirmField, 'Password123');
    await tester.pumpAndSettle();
    expect(find.text('Passwords match ✅'), findsOneWidget);
  });

  // Test for EnterRecoveryCode widget
  testWidgets('EnterRecoveryCode - renders code input and timer', (WidgetTester tester) async {
    bool onNextCalled = false;
    await tester.pumpWidget(MaterialApp(
      home: EnterRecoveryCode(
        enteredEmail: 'test@example.com',
        onNext: () {
          onNextCalled = true;
        },
      ),
    ));

    expect(find.text("We sent a validation code to "), findsOneWidget);
    expect(find.text("test@example.com"), findsOneWidget);
    expect(find.byType(FourDigitCodeField), findsOneWidget);

    final codeField = find.byType(FourDigitCodeField);
    await tester.enterText(codeField, '0000');
    await tester.pumpAndSettle();

    expect(find.text('Resend in 30 s'), findsOneWidget);

    final submitButton = find.widgetWithText(ElevatedButton, 'VALIDATE CODE');
    await tester.tap(submitButton);
    await tester.pumpAndSettle();

    expect(onNextCalled, false);  // onNext should not be called for invalid code

    await tester.enterText(codeField, '1234');
    await tester.pumpAndSettle();
    await tester.tap(submitButton);
    await tester.pumpAndSettle();

    expect(onNextCalled, true);  // onNext should be called for valid code
  });

  // Test for EnterRecoveryEmail widget
  testWidgets('EnterRecoveryEmail - renders and validates email', (WidgetTester tester) async {
    bool onNextCalled = false;
    String enteredEmail = '';
    await tester.pumpWidget(MaterialApp(
      home: EnterRecoveryEmail(
        enteredEmail: 'test@example.com',
        enterEmail: (email) {
          enteredEmail = email;
        },
        onNext: () {
          onNextCalled = true;
        },
      ),
    ));

    expect(find.text("Please enter the email associated to your account"), findsOneWidget);
    expect(find.byType(TextFormField), findsOneWidget);

    final emailField = find.byType(TextFormField);
    await tester.enterText(emailField, 'invalid-email');
    await tester.pumpAndSettle();

    expect(find.text('Please enter a valid email address'), findsOneWidget);

    final submitButton = find.widgetWithText(ElevatedButton, 'RECOVER PASSWORD');
    await tester.tap(submitButton);
    await tester.pumpAndSettle();

    expect(onNextCalled, false);  // onNext should not be called for invalid email

    await tester.enterText(emailField, 'valid@example.com');
    await tester.pumpAndSettle();
    await tester.tap(submitButton);
    await tester.pumpAndSettle();

    expect(onNextCalled, true);  // onNext should be called for valid email
    expect(enteredEmail, 'valid@example.com');
  });
}

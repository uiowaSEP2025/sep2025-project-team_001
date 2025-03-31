import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/create_account.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('Renders all input fields and labels', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    expect(find.text('Set up your account'), findsOneWidget);
    expect(find.text('Name'), findsOneWidget);
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Birthdate'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('Confirm Password'), findsOneWidget);
    expect(find.text("Create Account"), findsOneWidget);
  });

  testWidgets('Password validation logic and match feedback', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    await tester.enterText(find.byType(TextFormField).at(3), 'weak'); // Password
    await tester.pump();
    expect(find.textContaining('At least 8 characters'), findsOneWidget);

    await tester.enterText(find.byType(TextFormField).at(3), 'Strong1!');
    await tester.enterText(find.byType(TextFormField).at(4), 'Strong1!');
    await tester.pumpAndSettle();

    expect(find.text("Valid password ✅"), findsOneWidget);
    expect(find.text("Passwords match ✅"), findsOneWidget);
  });

  testWidgets('Terms checkbox toggles and enables create button when all valid', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    await tester.enterText(find.byType(TextFormField).at(0), 'Test User');
    await tester.enterText(find.byType(TextFormField).at(1), 'user@example.com');
    await tester.enterText(find.byType(TextFormField).at(2), '1990-01-01');
    await tester.enterText(find.byType(TextFormField).at(3), 'Strong1!');
    await tester.enterText(find.byType(TextFormField).at(4), 'Strong1!');
    await tester.tap(find.byType(Checkbox));
    await tester.pumpAndSettle();

    final button = tester.widget<ElevatedButton>(find.widgetWithText(ElevatedButton, "Create Account"));
    expect(button.onPressed != null, isTrue);
  });

  testWidgets('Clicking Terms and Conditions navigates', (WidgetTester tester) async {
    final navKey = GlobalKey<NavigatorState>();

    await tester.pumpWidget(MaterialApp(
      navigatorKey: navKey,
      routes: {'/terms': (_) => const Scaffold(body: Text('Terms Page'))},
      home: const CreateAccount(),
    ));

    await tester.tap(find.text('Terms and Conditions'));
    await tester.pumpAndSettle();

    expect(find.text('Terms Page'), findsOneWidget);
  });

  testWidgets('Displays error when email is invalid', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    await tester.enterText(find.byType(TextFormField).at(0), 'User');
    await tester.enterText(find.byType(TextFormField).at(1), 'invalid-email');
    await tester.enterText(find.byType(TextFormField).at(2), '1990-01-01');
    await tester.enterText(find.byType(TextFormField).at(3), 'Strong1!');
    await tester.enterText(find.byType(TextFormField).at(4), 'Strong1!');
    await tester.tap(find.byType(Checkbox));
    await tester.pumpAndSettle();

    // Tap create (should be disabled due to invalid email)
    final button = find.widgetWithText(ElevatedButton, 'Create Account');
    final buttonWidget = tester.widget<ElevatedButton>(button);
    expect(buttonWidget.onPressed, isNull); // still disabled
  });

  testWidgets('Invalid passwords do not allow submission', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    await tester.enterText(find.byType(TextFormField).at(3), 'abc');
    await tester.enterText(find.byType(TextFormField).at(4), 'abc');
    await tester.tap(find.byType(Checkbox));
    await tester.pump();

    expect(find.textContaining("At least 8 characters"), findsOneWidget);
    final button = tester.widget<ElevatedButton>(find.widgetWithText(ElevatedButton, "Create Account"));
    expect(button.onPressed, isNull);
  });

  testWidgets('Passwords mismatch shows feedback', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: CreateAccount()));

    await tester.enterText(find.byType(TextFormField).at(3), 'Strong1!');
    await tester.enterText(find.byType(TextFormField).at(4), 'WrongPass1!');
    await tester.pumpAndSettle();

    expect(find.text("Passwords do not match"), findsOneWidget);
  });
}

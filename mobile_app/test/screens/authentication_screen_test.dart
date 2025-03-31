// Test file for screens/authentication_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mockito/mockito.dart';

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

void main() {
  late MockNavigatorObserver mockObserver;

  setUp(() {
    mockObserver = MockNavigatorObserver();
  });

  Widget createWidgetUnderTest() {
    return MaterialApp(
      home: const AuthenticationPage(),
      navigatorObservers: [mockObserver],
      routes: {
        '/register': (_) => const Scaffold(body: Text("Register Page")),
        '/recover_password': (_) => const Scaffold(body: Text("Recover Page")),
        '/home': (_) => const Scaffold(body: Text("Home Page")),
      },
    );
  }

  testWidgets('renders email and password fields', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('LOGIN'), findsOneWidget);
    expect(find.text('Sign in'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('example@gmail.com'), findsOneWidget);
    expect(find.text('Forgot Password?'), findsOneWidget);

     await tester.tap(find.text('Forgot Password?'));

  });

  testWidgets('shows error if email or password is empty on login',
      (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    await tester.tap(find.text('LOGIN'));
    await tester.pump();

    expect(find.text('Please enter email and password'), findsOneWidget);
  });

  testWidgets('navigates to register screen on tap', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    await tester.tap(find.text('Sign Up'));
    await tester.pumpAndSettle();

    expect(find.text('Register Page'), findsOneWidget);
  });

  testWidgets('navigates to recover password screen on tap',
      (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    await tester.tap(find.text('Forgot Password?'));
    await tester.pumpAndSettle();

    expect(find.text('Recover Page'), findsOneWidget);
  });

  testWidgets('Sign in with Google and Apple buttons appear', (WidgetTester tester) async {
    await tester.pumpWidget(createWidgetUnderTest());

    expect(find.textContaining("Google"), findsOneWidget);
    expect(find.textContaining("Apple"), findsOneWidget);
  });
}

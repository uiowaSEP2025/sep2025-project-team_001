import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';
import '../helpers/fake_secure_storage.dart';
import '../mocks.mocks.dart';

void main() {
  final fakeStorage = FakeSecureStorage();
  TokenManager.init(storage: fakeStorage);
  testWidgets('Successful login shows snackbar and navigates to home',
      (WidgetTester tester) async {
    final mockDio = MockDio();

    when(mockDio.post('${ApiConfig.baseUrl}/mobile/login/',
            data: anyNamed('data'), options: anyNamed('options')))
        .thenAnswer((_) async {
      print('call made');
      return Response(
        data: {
          'tokens': {
            'access': 'fake_access_token',
            'refresh': 'fake_refresh_token',
          },
          'customer_id': 1
        },
        statusCode: 200,
        requestOptions: RequestOptions(path: ''),
      );
    });

    await tester.pumpWidget(
      MaterialApp(
        home: AuthenticationPage(dio: mockDio),
        onGenerateRoute: (settings) {
          print('Navigating to: ${settings.name}');

          if (settings.name == '/home') {
            return MaterialPageRoute(
              builder: (_) => const Scaffold(
                body: Center(child: Text('Home Page')),
              ),
            );
          }
          return null;
        },
      ),
    );

    await tester.enterText(find.byType(TextField).at(0), 'test@email.com');
    await tester.enterText(find.byType(TextField).at(1), 'Password1!');
    await tester.tap(find.text('LOGIN'));

    await tester.pumpAndSettle(const Duration(seconds: 2));

    expect(find.text('Login successful!'), findsOneWidget);

    expect(find.text('Home Page'), findsOneWidget);
  });

  testWidgets('No email entered', (WidgetTester tester) async {
    debugDefaultTargetPlatformOverride = TargetPlatform.iOS;
    final mockDio = MockDio();

    await tester.pumpWidget(
      MaterialApp(
        home: AuthenticationPage(dio: mockDio),
      ),
    );

    await tester.tap(find.text('Sign In with Apple'));
    await tester.tap(find.text('LOGIN'));

    await tester.pumpAndSettle(const Duration(seconds: 2));

    expect(find.text('Please enter email and password'), findsOneWidget);
    debugDefaultTargetPlatformOverride = null;
  });

  testWidgets('Click signup', (WidgetTester tester) async {
    final mockDio = MockDio();

    await tester.pumpWidget(
      MaterialApp(
        home: AuthenticationPage(dio: mockDio),
        onGenerateRoute: (settings) {
          print('Navigating to: ${settings.name}');

          if (settings.name == '/register') {
            return MaterialPageRoute(
              builder: (_) => const Scaffold(
                body: Center(child: Text('Sign up Page')),
              ),
            );
          }
          return null;
        },
      ),
    );

    await tester.ensureVisible(find.byKey(const Key('signUpButton')));
    await tester.tap(find.byKey(const Key('signUpButton')));

    await tester.pumpAndSettle(const Duration(seconds: 2));

    expect(find.text('Sign up Page'), findsOneWidget);
  });

  testWidgets('Click Forgot password', (WidgetTester tester) async {
    final mockDio = MockDio();

    await tester.pumpWidget(
      MaterialApp(
        home: AuthenticationPage(dio: mockDio),
        onGenerateRoute: (settings) {
          print('Navigating to: ${settings.name}');

          if (settings.name == '/recover_password') {
            return MaterialPageRoute(
              builder: (_) => const Scaffold(
                body: Center(child: Text('Password Page')),
              ),
            );
          }
          return null;
        },
      ),
    );

    await tester.tap(find.text('Forgot Password?'));
    await tester.pumpAndSettle(const Duration(seconds: 2));

    expect(find.text('Password Page'), findsOneWidget);
  });
}

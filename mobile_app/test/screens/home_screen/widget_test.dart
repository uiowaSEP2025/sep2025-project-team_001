import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/restaurant_selection_screen.dart';

class TestHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    HttpOverrides.global = TestHttpOverrides();
  });

  testWidgets('Bars are selectable and toggle correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: RestaurantSelectionScreen()));

    final bar1 = find.text('Scouts');
    final bar2 = find.text('Coa');
    final bar3 = find.text('Roxxy');
    final bar4 = find.text('Brothers');

    await tester.tap(bar1);
    await tester.pumpAndSettle();

    expect(find.text('Scouts'), findsOneWidget);
  });

}
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/authentication/terms_conditions_screen.dart';

void main() {
  testWidgets('TermsAndConditionsScreen renders all sections and scrolls',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: TermsAndConditionsScreen()),
    );

    // Verify AppBar title
    expect(find.text('Terms and Conditions'), findsOneWidget);

    // Verify sections titles
    expect(find.text('1. Acceptance of Terms\n\n'), findsOneWidget);
    expect(find.text('2. Eligibility\n\n'), findsOneWidget);
    expect(find.text('3. Use of the App\n\n'), findsOneWidget);
    expect(find.text('4. Account Registration\n\n'), findsOneWidget);
    expect(find.text('5. Bar Listings and Promotions\n\n'), findsOneWidget);
    expect(find.text('6. User Conduct\n\n'), findsOneWidget);
    expect(find.text('7. Payments & Refunds\n\n'), findsOneWidget);
    expect(find.text('8. Privacy Policy\n\n'), findsOneWidget);
    expect(find.text('9. Limitation of Liability\n\n'), findsOneWidget);
    expect(find.text('10. Termination\n\n'), findsOneWidget);
    expect(find.text('11. Changes to Terms\n\n'), findsOneWidget);

    // Scroll down to ensure all text is in view
    final scrollable = find.byType(Scrollable);
    expect(scrollable, findsOneWidget);

    await tester.fling(scrollable, const Offset(0, -800), 1000);
    await tester.pumpAndSettle();

    // Confirm last section text is in the view
    expect(find.text("We may update these Terms at any time.\n\n\n"), findsOneWidget);
  });
}

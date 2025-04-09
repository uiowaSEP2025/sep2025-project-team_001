import 'package:flutter/material.dart';
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mobile_app/authentication/create_account.dart';
import 'package:mobile_app/authentication/recover_email/recover_password.dart';
import 'package:mobile_app/authentication/terms_conditions_screen.dart';
import 'package:mobile_app/home/restaurant/restaurant_menu_screen.dart';
import 'package:mobile_app/home/restaurant_addition_screen.dart';
import 'package:mobile_app/main_navigation/main_navigation_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  Stripe.publishableKey =
      'pk_test_51RAFr02cTgsJM4b11a6uRlyWLHp0qyDzpf7FnNvBdWC15nc7r0UGfmgDTUBgaK3thLKa6OXRGtufqo69pXRz6ikT00EWGzhEwv';
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Streamline',
      initialRoute: '/',
      onGenerateRoute: (RouteSettings settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(
                builder: (_) => const AuthenticationPage());
          // case '/home':
          //   return MaterialPageRoute(
          //       builder: (_) => const RestaurantSelectionScreen());
          case '/home':
            final args = settings.arguments as Map<String, dynamic>?;
            final initialIndex = args?['initialIndex'] ?? 0;

            return MaterialPageRoute(
              builder: (_) => MainNavigationScreen(initialIndex: initialIndex),
            );

          case '/register':
            return MaterialPageRoute(builder: (_) => const CreateAccount());
          case '/terms':
            return MaterialPageRoute(
                builder: (_) => const TermsAndConditionsScreen());
          case '/recover_password':
            return MaterialPageRoute(
                builder: (_) => const RecoverPasswordScreen());
          case '/add_restaurant':
            return MaterialPageRoute(
                builder: (_) => const RestaurantAdditionScreen());
          case '/home/restaurant_menu':
            final args = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (_) => RestaurantMenuScreen(
                restaurant: args['restaurant'],
              ),
              settings: settings,
            );
          default:
            return MaterialPageRoute(
              builder: (_) => const Scaffold(
                body: Center(child: Text('Page not found')),
              ),
            );
        }
      },
    );
  }
}

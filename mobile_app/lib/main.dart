import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mobile_app/authentication/create_account.dart';
import 'package:mobile_app/authentication/recover_email/recover_password.dart';
import 'package:mobile_app/authentication/terms_conditions_screen.dart';
import 'package:mobile_app/home/restaurant/restaurant_menu_screen.dart';
import 'package:mobile_app/home/restaurant_addition_screen.dart';
import 'package:mobile_app/main_navigation/main_navigation_screen.dart';
import 'package:mobile_app/main_navigation/orders/order_history_screen.dart';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

  RemoteMessage? initialMessage =
      await FirebaseMessaging.instance.getInitialMessage();
  if (initialMessage != null) {
    _handleMessageNavigation(initialMessage);
  }

  FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
    _handleMessageNavigation(message);
  });

  Stripe.publishableKey =
      'pk_test_51RAFr02cTgsJM4b11a6uRlyWLHp0qyDzpf7FnNvBdWC15nc7r0UGfmgDTUBgaK3thLKa6OXRGtufqo69pXRz6ikT00EWGzhEwv';

  runApp(const MyApp());
}

Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();

  print("Background Message: ${message.notification?.title}");
}

void _handleMessageNavigation(RemoteMessage message) {
  final data = message.data;

  if (data['type'] == 'ORDER_UPDATE' && data['order_id'] != null) {
    navigatorKey.currentState?.pushNamedAndRemoveUntil(
      '/home',
      (route) => false,
      arguments: {'initialIndex': 1},
    );
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: navigatorKey,
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
          case '/orders/order_history':
            final args = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (_) => OrderHistoryScreen(
                pickedUpOrders: args['orders'],
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

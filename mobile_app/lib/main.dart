import 'package:flutter/material.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mobile_app/authentication/create_account.dart';
import 'package:mobile_app/authentication/recover_email/recover_password.dart';
import 'package:mobile_app/authentication/terms_conditions_screen.dart';
import 'package:mobile_app/home/restaurant_addition_screen.dart';
import 'package:mobile_app/home/restaurant_selection_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
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
      routes: {
        '/': (context) => const AuthenticationPage(), 
        '/home' : (context) => const RestaurantSelectionScreen(),
        '/register' : (context) => const CreateAccount(),
        '/terms' : (context) => const TermsAndConditionsScreen(),
        '/recover_password' : (context) => const RecoverPasswordScreen(),
        '/add_restaurant' : (context) => const RestaurantAdditionScreen()
        // '/settings' : (context) => 
        }
      
    );
  }
}


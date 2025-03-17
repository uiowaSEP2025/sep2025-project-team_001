import 'package:flutter/material.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mobile_app/authentication/create_account.dart';
import 'package:mobile_app/home/bar_selection_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Streamline',
      initialRoute: '/home',
      routes: {
        '/': (context) => AuthenticationPage(), 
        '/home' : (context) => BarSelectionScreen(),
        '/register' : (context) => CreateAccount(),
        }
      
    );
  }
}


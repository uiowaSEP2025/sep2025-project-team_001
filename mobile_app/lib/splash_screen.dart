import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mobile_app/api_services.dart';
import 'package:mobile_app/main.dart';
import 'package:mobile_app/utils/user_manager.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _checkAuthentication();
  }

  Future<void> _checkAuthentication() async {
    final email = await UserManager.getEmail();
    final password = await UserManager.getPassword();

    if (email != null && password != null) {
      try {
        await authenticate(email, password);
        navigatorKey.currentState?.pushReplacementNamed(
          '/home',
          arguments: {'initialIndex': 0},
        );
      } catch (e) {
        navigatorKey.currentState?.pushReplacementNamed('/authentication');
      }
    } else {
      navigatorKey.currentState?.pushReplacementNamed('/authentication');
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: CircularProgressIndicator()),
    );
  }
}

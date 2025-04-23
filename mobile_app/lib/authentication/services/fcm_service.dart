import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';

void registerFcmToken(int customerId) async {
  final accessToken = await TokenManager.getAccessToken();

  FirebaseMessaging messaging = FirebaseMessaging.instance;
  await messaging.requestPermission();

  String? token = await messaging.getToken();
  print("FCM token: $token");
  if (token != null) {
    const String endpoint = "${ApiConfig.baseUrl}/mobile/fcm_token/";

    final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

    final body = {
      'customer_id': customerId,
      'fcm_token': token,
    };

    try {
      final response = await dio.post(
        endpoint,
        data: jsonEncode(body),
        options: Options(
          headers: {
            "Authorization": "Bearer $accessToken",
            "Content-Type": "application/json",
          },
        ),
      );
    } on DioException catch (e) {
      print("Error sending firebase token: ${e.response?.data}");
      throw Exception(
          "Error sending firebase token: ${e.response?.statusCode}");
    }
  }
}

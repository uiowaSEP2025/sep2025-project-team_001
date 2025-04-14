import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';

void registerFcmToken(int customerId) async {
    final accessToken = await TokenManager.getAccessToken();

  FirebaseMessaging messaging = FirebaseMessaging.instance;
  String? token = await messaging.getToken();

  if (token != null) {
    const String endpoint = "${ApiConfig.baseUrl}/save_fcm_token/";

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

      if (response.statusCode == 201) {
        print("Order placed! ID: ${response.data['order_id']}");
        final orderId = response.data['order_id'];
        return orderId;
      } else {
        print("Failed to place order: ${response.data}");
        throw Exception("Failed to place order");
      }
    } on DioException catch (e) {
      print("Order error: ${e.response?.data}");
      throw Exception("Error placing order: ${e.response?.statusCode}");
    }
  }
}

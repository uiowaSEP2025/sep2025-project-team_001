import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:mobile_app/api_services.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/utils/token_manager.dart';

Future<int> cancelOrder(
    {required int orderId, required int restaurantId}) async {
  final accessToken = await TokenManager.getAccessToken();

  if (accessToken == null) {
    throw Exception('Access token not found');
  }
  final String endpoint =
      "${ApiConfig.baseUrl}/orders/$restaurantId/$orderId/cancelled/";
  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  try {
    final response = await dio.patch(
      endpoint,
      options: Options(
        headers: {
          "Authorization": "Bearer $accessToken",
          "Content-Type": "application/json",
        },
      ),
    );

    if (response.statusCode == 200) {
      print("Order cancelled! ID: ${response.data['order_id']}");
      final orderId = response.data['order_id'];
      return orderId;
    } else {
      print("Failed to cancel order: ${response.data}");
      throw Exception("Failed to cancel order");
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await cancelOrder(orderId: orderId,restaurantId: restaurantId);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("Order error: ${e.response?.data}");
    throw Exception("Error cancelling order: ${e.response?.statusCode}");
  }
}

Future<int> reviewOrder(
    {required int orderId, required double rating, required String review}) async {
  final accessToken = await TokenManager.getAccessToken();

  if (accessToken == null) {
    throw Exception('Access token not found');
  }
  const String endpoint = "${ApiConfig.baseUrl}/mobile/review/create";

  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  final body = {
    'order': orderId,
    'rating': rating,
    'comment': review,
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
      print("Review created!");
      final orderId = response.data['order'];
      return orderId;
    } else {
      print("Failed to review order: ${response.statusCode}");
      throw Exception("Failed to review order");
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();

      if (refreshed) {
        return await reviewOrder(orderId: orderId, rating: rating, review: review);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("Order error: ${e.response?.data}");
    throw Exception("Error reviewing order: ${e.response?.statusCode}");
  }
}

Future<Order> getOrder(
    {required int orderId}) async {
  final accessToken = await TokenManager.getAccessToken();

  if (accessToken == null) {
    throw Exception('Access token not found');
  }
  final String endpoint = "${ApiConfig.baseUrl}/order/$orderId/";

  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  try {
    final response = await dio.get(
      endpoint,
      options: Options(
        headers: {
          "Authorization": "Bearer $accessToken",
          "Content-Type": "application/json",
        },
      ),
    );

    if (response.statusCode == 200) {
      final order = Order.fromJson(response.data);
      return order;
    } else {
      print("Failed to get order: ${response.statusCode}");
      throw Exception("Failed to get order");
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();

      if (refreshed) {
        return await getOrder(orderId: orderId);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("Order error: ${e.response?.data}");
    throw Exception("Error getting order: ${e.response?.statusCode}");
  }
}
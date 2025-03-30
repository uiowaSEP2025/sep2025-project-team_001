import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';

Future<List<Restaurant>> fetchCustomerRestaurants() async {


  return [];
}


  Future<List<Restaurant>> fetchRestaurants() async { //todo move to its own service folder bc it is only accessing the api
    final accessToken = await TokenManager.getAccessToken();

    if (accessToken == null) {
      throw Exception('Access token not found');
    }

    final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));
    const String endpoint = "${ApiConfig.baseUrl}/restaurants/list";

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

      final data = response.data as List<dynamic>;
      return data.map((json) => Restaurant.fromJson(json)).toList();
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception("Access token expired or unauthorized");
      }

      print("Fetch restaurants error: ${e.response?.data}");
      throw Exception("Failed to fetch restaurants: ${e.response?.statusCode}");
    }
  }


  Future<int> placeOrder({
    required int customerId,
    required int restaurantId,
    required Map<String, CartItem> cart,
  }) async {
    final accessToken = await TokenManager.getAccessToken();

    if (accessToken == null) {
      throw Exception('Access token not found');
    }

    const String endpoint = "${ApiConfig.baseUrl}/order/new/";
    final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

    final orderItems = cart.values.map((cartItem) {
      return {
        'item_id': cartItem.item.id,
        'quantity': cartItem.quantity,
      };
    }).toList();

    final body = {
      'customer_id': customerId,
      'restaurant_id': restaurantId,
      'order_items': orderItems,
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

Future<List<Order>> fetchUserOrders(int customerId) async {
  final accessToken = await TokenManager.getAccessToken();
  final dio = Dio();

  const String endpoint = "${ApiConfig.baseUrl}/order/customer/";

  final response = await dio.get(
    endpoint,
    options: Options(
      headers: {
        "Authorization": "Bearer $accessToken",
        "Content-Type": "application/json",
      },
    ),
  );

  final data = response.data as List;
  return data.map((json) => Order.fromJson(json)).toList();
}

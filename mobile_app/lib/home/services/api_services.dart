import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:mobile_app/api_services.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/main.dart';
import 'package:mobile_app/utils/token_manager.dart';

Future<List<Restaurant>> fetchCustomerRestaurants() async {
  return [];
}

Future<List<Restaurant>> fetchRestaurants() async {
  final accessToken = await TokenManager.getAccessToken();

  if (accessToken == null) {
    throw Exception('Access token not found');
  }

  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));
  const String endpoint = "${ApiConfig.baseUrl}/restaurants/list/";

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
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await fetchRestaurants();
      }
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
      'unwanted_ingredients': cartItem.unwantedIngredientsIds,
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
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await placeOrder(
            customerId: customerId, restaurantId: restaurantId, cart: cart);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("Order error: ${e.response?.data}");
    throw Exception("Error placing order: ${e.response?.statusCode}");
  }
}

Future<List<Order>> fetchUserOrders(int customerId) async {
  final accessToken = await TokenManager.getAccessToken();
  final dio = Dio();

  const String endpoint = "${ApiConfig.baseUrl}/order/customer/";
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
      final data = response.data as List;
      print(data);
      return data.map((json) => Order.fromJson(json)).toList();
    } else {
      throw Exception("Failed to fetch user orders");
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await fetchUserOrders(customerId);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("PaymentIntent error: ${e.response?.data}");
    throw Exception("Error creating PaymentIntent: ${e.response?.statusCode}");
  }
}

Future<Map<String, String>> createPaymentIntent(double amountInDollars,
    {bool saveCard = false}) async {
  final accessToken = await TokenManager.getAccessToken();

  if (accessToken == null) {
    throw Exception('Access token not found');
  }

  const String endpoint = "${ApiConfig.baseUrl}/order/payment/";
  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  try {
    final response = await dio.post(
      endpoint,
      data: jsonEncode({
        'amount': (amountInDollars * 100).toInt(),
        'save_card': saveCard,
      }),
      options: Options(
        headers: {
          "Authorization": "Bearer $accessToken",
          "Content-Type": "application/json",
        },
      ),
    );

    if (response.statusCode == 200) {
      final clientSecret = response.data['client_secret'];
      final customerId = response.data['customer_id'];
      return {
        'clientSecret': clientSecret,
        'customerId': customerId,
      };
    } else {
      throw Exception("Failed to create PaymentIntent");
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await createPaymentIntent(amountInDollars);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("PaymentIntent error: ${e.response?.data}");
    throw Exception("Error creating PaymentIntent: ${e.response?.statusCode}");
  }
}

Future<bool> handleCheckout(double amount) async {
  final accessToken = await TokenManager.getAccessToken();

  final methodsResponse = await Dio().get(
    "${ApiConfig.baseUrl}/order/payment/methods/",
    options: Options(headers: {
      "Authorization": "Bearer $accessToken",
    }),
  );

  final savedMethods = methodsResponse.data['paymentMethods'];

  try {
    if (savedMethods.isEmpty) {
      final saveCard = await showDialog<bool>(
        context: navigatorKey.currentContext!,
        builder: (context) => AlertDialog(
          title: Text("Save your card?"),
          content: Text(
              "Would you like to securely save your card for faster future checkouts?"),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: Text("No"),
            ),
            ElevatedButton(
              onPressed: () => Navigator.of(context).pop(true),
              child: Text("Yes"),
            ),
          ],
        ),
      );

      if (saveCard == true) {
        final stripeData = await createPaymentIntent(amount, saveCard: true);

        await Stripe.instance.initPaymentSheet(
          paymentSheetParameters: SetupPaymentSheetParameters(
            paymentIntentClientSecret: stripeData['clientSecret'],
            customerId: stripeData['customerId'],
            merchantDisplayName: 'Streamline',
          ),
        );

        await Stripe.instance.presentPaymentSheet();
      } else {
        final stripeData = await createPaymentIntent(amount, saveCard: false);

        await Stripe.instance.initPaymentSheet(
          paymentSheetParameters: SetupPaymentSheetParameters(
            paymentIntentClientSecret: stripeData['clientSecret'],
            merchantDisplayName: 'Streamline',
          ),
        );

        await Stripe.instance.presentPaymentSheet();
      }
    } else {
      final selectedCardId = await showCardPicker(savedMethods);

      if (selectedCardId != null) {
        await payWithSavedCard(selectedCardId, amount);
      } else {
        print("User canceled card selection.");
        return false;
      }
    }

    return true;
  } catch (e) {
    print("Payment error inside handleCheckout: $e");
    return false;
  }
}

Future<void> payWithSavedCard(String paymentMethodId, double amount) async {
  final accessToken = await TokenManager.getAccessToken();

try{
  final response = await Dio().post(
    "${ApiConfig.baseUrl}/order/payment/saved_card/",
    data: {
      "payment_method_id": paymentMethodId,
      "amount": (amount * 100).toInt(),
    },
    options: Options(headers: {
      "Authorization": "Bearer $accessToken",
      "Content-Type": "application/json",
    }),
  );

  if (response.statusCode == 200) {
    print("Payment successful!");
  } else {
    print("Payment failed: ${response.data}");
  }}
  on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await payWithSavedCard(paymentMethodId,amount);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("PaymentIntent error: ${e.response?.data}");
    throw Exception("Error creating PaymentIntent: ${e.response?.statusCode}");
  }
}

Future<void> deletePaymentMethod(String paymentMethodId) async {
  final accessToken = await TokenManager.getAccessToken();

  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  try {
    final response = await dio.delete(
      "${ApiConfig.baseUrl}/order/payment/saved_card/$paymentMethodId/",
      options: Options(
        headers: {
          "Authorization": "Bearer $accessToken",
          "Content-Type": "application/json",
        },
      ),
    );

    if (response.statusCode == 200) {
      print('Payment method deleted successfully');
      ScaffoldMessenger.of(navigatorKey.currentContext!).showSnackBar(
        SnackBar(content: Text('Payment method deleted')),
      );
    } else {
      print('Failed to delete payment method');
    }
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      final refreshed = await refreshAccessToken();
      if (refreshed) {
        return await deletePaymentMethod(paymentMethodId);
      }
      throw Exception("Access token expired or unauthorized");
    }
    print("Delete error: ${e.response?.data}");
  }
}

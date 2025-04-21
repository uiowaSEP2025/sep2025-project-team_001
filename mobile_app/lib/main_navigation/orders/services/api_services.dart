import 'package:dio/dio.dart';
import 'package:mobile_app/constants.dart';
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
    print("Order error: ${e.response?.data}");
    throw Exception("Error cancelling order: ${e.response?.statusCode}");
  }
}

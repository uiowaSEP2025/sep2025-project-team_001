import 'package:dio/dio.dart';
import 'package:mobile_app/classes/bar.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';

Future<List<Restaurant>> fetchCustomerRestaurants() async {
  return [
    Restaurant(
        name: "sep new",
        address: "Scouts avenue",
        phone: "1111111111"
            "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FbrothersLogo.png?alt=media&token=d4b583ee-2fb5-499a-b3a2-04196ff68f98"),
  ];

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

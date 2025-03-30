import 'package:dio/dio.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';
import 'package:mobile_app/utils/token_manager.dart';

Future<List<MenuItem>> fetchMenuItems(String restaurantName) async {
  final accessToken = await TokenManager.getAccessToken();
  print(accessToken);
  if (accessToken == null) {
    throw Exception('Access token not found');
  }

  final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));
  final String endpoint =
      "${ApiConfig.baseUrl}/restaurants/$restaurantName/menu/";

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
    print(data.map((json) => MenuItem.fromJson(json)));
    return data.map((json) => MenuItem.fromJson(json)).toList();
  } on DioException catch (e) {
    if (e.response?.statusCode == 401) {
      throw Exception("Access token expired or unauthorized");
    }

    print("Fetch menu error: ${e.response?.data}");
    throw Exception("Failed to fetch menu: ${e.response?.statusCode}");
  }
}

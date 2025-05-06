import 'package:dio/dio.dart';
import 'package:mobile_app/authentication/services/fcm_service.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';
import 'package:mobile_app/utils/user_manager.dart';

Future<bool> refreshAccessToken() async {
    final refreshToken = await TokenManager.getRefreshToken();

  if (refreshToken == null) {
    return false;
  }

    final dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

  try {
    final response = await dio.post(
      '${ApiConfig.baseUrl}/token/refresh/',
      data: {
        'refresh': refreshToken,
      },
    );

    if (response.statusCode == 200) {
      final newAccessToken = response.data['access'];
      await TokenManager.saveTokens(newAccessToken, refreshToken);
      return true;
    } else {
      return false;
    }
  } catch (e) {
    print('Error refreshing token: $e');
    return false;
  }
}

Future<void> authenticate(String email, String password) async{

  
    const String endpoint = "${ApiConfig.baseUrl}/mobile/login/";

  try {
      final dio = 
          Dio(BaseOptions(connectTimeout: const Duration(seconds: 10)));

      final response = await dio.post(
        endpoint,
        data: {
          "username": email,
          "password": password,
        },
        options: Options(headers: {"Content-Type": "application/json"}),
      );

      final tokens = response.data['tokens'];
      final accessToken = tokens['access'];
      final refreshToken = tokens['refresh'];

      final userId = response.data['customer_id'];

      print(response);

      final userName = response.data['name'];

      await UserManager.saveUser(userId);

      print(userId);
      print(userName);

      await TokenManager.saveTokens(accessToken, refreshToken);
      await UserManager.saveName(userName);

      registerFcmToken(userId);

    } on DioException catch (e) {
      String errorMessage = "Authentication failed";

      print("Login error: ${e.response?.data}");
      print("Status code: ${e.response?.statusCode}");

      if (e.response?.data is Map && e.response?.data['error'] != null) {
        errorMessage = e.response!.data['error'];
      } else if (e.response?.data is Map) {
        errorMessage = e.response!.data.toString();
      }

      throw Exception(errorMessage);
    }
}

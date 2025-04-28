import 'package:dio/dio.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/utils/token_manager.dart';

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

import 'package:dio/dio.dart';
import 'package:mobile_app/constants.dart';

class AuthService {
  final Dio dio;

  AuthService({Dio? dio}) : dio = dio ?? Dio();

  Future<Map<String, dynamic>> login(String email, String password) async {

    const String endpoint = "${ApiConfig.baseUrl}/mobile/login/";

    final response = await dio.post(
      endpoint,
      data: {"username": email, "password": password},
      options: Options(headers: {"Content-Type": "application/json"}),
    );

    return response.data;
  }
}

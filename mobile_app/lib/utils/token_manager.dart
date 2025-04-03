import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenManager {
  static FlutterSecureStorage _storage = const FlutterSecureStorage();

  // Allows injection of a mock for testing
  static void init({FlutterSecureStorage? storage}) {
    _storage = storage ?? const FlutterSecureStorage();
  }

  static Future<void> saveTokens(String access, String refresh) async {
    await _storage.write(key: 'access', value: access);
    await _storage.write(key: 'refresh', value: refresh);
  }

  static Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access');
  }

  static Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'refresh');
  }

  static Future<void> clearTokens() async {
    await _storage.delete(key: 'access');
    await _storage.delete(key: 'refresh');
  }
}

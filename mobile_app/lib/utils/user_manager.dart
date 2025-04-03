import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class UserManager {
  static const _storage = FlutterSecureStorage();

  static Future<void> saveUser(int customerId) async {
    await _storage.write(key: 'userId', value: customerId.toString());
  }

  static Future<int?> getUser() async {
    final userIdStr = await _storage.read(key: 'userId');
    if (userIdStr == null) return null;
    return int.tryParse(userIdStr);
  }

  static Future<void> clearUser() async {
    await _storage.delete(key: 'userId');
  }
}

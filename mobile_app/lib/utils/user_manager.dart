import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class UserManager {
  static const _storage = FlutterSecureStorage();

  static Future<void> saveUser(int customerId) async{
    await _storage.write(key: 'userId', value: customerId.toString());
  }

  static Future<void> saveEmail(String userEmail) async{
    await _storage.write(key: 'userEmail', value: userEmail);
  }

 static Future<void> saveName(String userName) async{
    await _storage.write(key: 'userName', value: userName);
  }

static Future<int?> getUser() async {
  final userIdStr = await _storage.read(key: 'userId');
  if (userIdStr == null) return null;
  return int.tryParse(userIdStr);
}

  static Future<void> clearUser() async {
    await _storage.delete(key: 'userId');
  }

  static Future<String?> getEmail() async {
   return await _storage.read(key: 'userEmail');
  }

  static Future<String?> getName() async {
   return await _storage.read(key: 'userName');
  }

  static Future<void> clearEmail() async {
    await _storage.delete(key: 'userEmail');
  }

  static Future<void> clearName() async {
    await _storage.delete(key: 'userName');
  }
}

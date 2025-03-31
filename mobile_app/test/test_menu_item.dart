import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';

void main() {
  group('MenuItem model', () {
    test('fromJson should return correct instance', () {
      final json = { 'id': 1, 'name': 'Sample', 'description': 'desc', 'price': 5.0, 'category': 'main', 'available': true };
      final model = MenuItem.fromJson(json);
      expect(model.id, 1);
    });
  });
}
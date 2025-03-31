import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/home/restaurant/models/order.dart';

void main() {
  group('Order model', () {
    test('fromJson should return correct instance', () {
      final json = { 'id': 1, 'name': 'Sample', 'description': 'desc', 'price': 5.0, 'category': 'main', 'available': true };
      final model = Order.fromJson(json);
      expect(model.id, 1);
    });
  });
}
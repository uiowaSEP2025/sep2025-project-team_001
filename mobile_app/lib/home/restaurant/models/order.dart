import 'package:mobile_app/home/restaurant/models/restaurant.dart';

class Order {
  final int id;
  final String startTime;
  final List<dynamic> items;
  final String status;
  final double totalPrice;
  final int restaurantId;
  final String restaurantName;

  Order(
      {required this.id,
      required this.startTime,
      required this.items,
      required this.status,
      required this.totalPrice,
       required this.restaurantId,
       required this.restaurantName});

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
        id: json['id'],
        startTime: json['start_time'],
        items: json['order_items'] ?? [],
        status: json['status'],
        totalPrice: json['total_price'],
        restaurantId: json['restaurant_id'],
        restaurantName: json['restaurant_name']);
  }
}

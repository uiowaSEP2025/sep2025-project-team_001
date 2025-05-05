import 'package:mobile_app/home/restaurant/models/restaurant.dart';

class Order {
  final int id;
  final String startTime;
  final List<dynamic> items;
  final String status;
  final double totalPrice;
  final int restaurantId;
  final String restaurantName;
  final int? foodETAminutes;
  final int? drinksETAminutes;
  final bool reviewed;
  final String foodStatus;
  final String drinkStatus;

  Order(
      {required this.id,
      required this.startTime,
      required this.items,
      required this.status,
      required this.totalPrice,
      required this.restaurantId,
      required this.restaurantName,
      this.foodETAminutes,
      this.drinksETAminutes,
      required this.reviewed,
      required this.foodStatus,
      required this.drinkStatus});

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
        id: json['id'],
        startTime: json['start_time'],
        items: json['order_items'] ?? [],
        status: json['status'],
        totalPrice: json['total_price'],
        restaurantId: json['restaurant_id_read'],
        restaurantName: json['restaurant_name'],
        foodETAminutes: json['food_eta_minutes'],
        drinksETAminutes: json['beverage_eta_minutes'],
        reviewed: json['reviewed'],
        foodStatus: json['food_status'],
        drinkStatus: json['beverage_status']);
  }
}

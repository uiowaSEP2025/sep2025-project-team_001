import 'package:intl/intl.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';

class Order {
  final int id;
  final String startTime;
  final List<dynamic> items;
  final String status;
  final double totalPrice;
  final int restaurantId;
  final String restaurantName;
  final String? foodETAminutes;
  final String? drinksETAminutes;
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

    String? formatTime(String? dateTimeString) {
      if (dateTimeString == null) return null;
      try {
        final time = DateTime.parse(dateTimeString);
        final localTime = time.toLocal();
        return DateFormat.jm().format(localTime);
      } catch (_) {
        return null;
      }
    }

    return Order(
        id: json['id'],
        startTime: json['start_time'],
        items: json['order_items'] ?? [],
        status: json['status'],
        totalPrice: json['total_price'],
        restaurantId: json['restaurant_id_read'],
        restaurantName: json['restaurant_name'],
        foodETAminutes: formatTime(json['estimated_food_ready_time']),
        drinksETAminutes: formatTime(json['estimated_beverage_ready_time']),
        reviewed: json['reviewed'],
        foodStatus: json['food_status'],
        drinkStatus: json['beverage_status']);
  }
}

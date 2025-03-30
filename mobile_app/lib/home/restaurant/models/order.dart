class Order {
  final int id;
  final String startTime;
  final List<dynamic> items; // Or use a specific model if available

  Order({
    required this.id,
    required this.startTime,
    required this.items,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      startTime: json['start_time'],
      items: json['order_items'] ?? [],
    );
  }
}

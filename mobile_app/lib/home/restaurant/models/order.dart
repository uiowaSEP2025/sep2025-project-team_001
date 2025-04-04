class Order {
  final int id;
  final String startTime;
  final List<dynamic> items;
  final String status;
  final double totalPrice;

  Order(
      {required this.id,
      required this.startTime,
      required this.items,
      required this.status,
      required this.totalPrice});

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
        id: json['id'],
        startTime: json['start_time'],
        items: json['order_items'] ?? [],
        status: json['status'] ?? 'pending',
        totalPrice: json['total_price']);
  }
}

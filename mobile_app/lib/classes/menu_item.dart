class MenuItem {
  final String name;
  final String description;
  final double price;
  final String category;
  final bool available;

  MenuItem({
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    required this.available,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      name: json['name'],
      description: json['description'] ?? '',
      price: double.parse(json['price']),
      category: json['category'] ?? 'Other',
      available: json['available'],
    );
  }
}

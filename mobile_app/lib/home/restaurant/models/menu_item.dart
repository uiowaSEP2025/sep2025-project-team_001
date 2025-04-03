class MenuItem {
  final int id;
  final String name;
  final String description;
  final double price;
  final String category;
  final bool available;
  final String? base64image;

  MenuItem({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    required this.available,
    this.base64image,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      id: json['id'],
      name: json['name'],
      description: json['description'] ?? '',
      price: json['price'],
      category: json['category'] ?? 'Other',
      available: json['available'],
      base64image: json['base64_image'],
    );
  }
}

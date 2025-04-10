class MenuItem {
  final int id;
  final String name;
  final String description;
  final double price;
  final String category;
  final bool available;
  final String? base64image;
  final List<Ingredient> ingredients;

  MenuItem({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    required this.available,
    this.base64image,
    required this.ingredients,
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
      ingredients: (json['ingredients'] as List<dynamic>?)
              ?.map((i) => Ingredient.fromJson(i))
              .toList() ??
          [],
    );
  }
}

class Ingredient {
  final int id;
  final String name;

  Ingredient({required this.id, required this.name});

  factory Ingredient.fromJson(Map<String, dynamic> json) {
    return Ingredient(
      id: json['id'],
      name: json['name'],
    );
  }
}

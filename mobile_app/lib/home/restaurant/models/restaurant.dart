class Restaurant {
  final String name;
  final String address;
  final String phone;
  final int id;
  final String? base64image;

  Restaurant({
    required this.id,
    required this.name,
    required this.address,
    required this.phone,
    this.base64image,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      address: json['address'],
      phone: json['phone'],
      base64image: json['restaurant_image'],
    );
  }
}

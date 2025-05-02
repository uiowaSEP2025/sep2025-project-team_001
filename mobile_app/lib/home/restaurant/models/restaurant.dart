class Restaurant {
  final String name;
  final String address;
  final String phone;
  final int id;
  final String? restaurantImageUrl;

  Restaurant({
    required this.id,
    required this.name,
    required this.address,
    required this.phone,
    this.restaurantImageUrl,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      address: json['address'],
      phone: json['phone'],
      restaurantImageUrl: json['restaurant_image_url'],
    );
  }
}

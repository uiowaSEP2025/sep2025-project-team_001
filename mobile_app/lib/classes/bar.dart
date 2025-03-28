class Restaurant {
  final String name;
  final String address;
  final String phone;

  Restaurant({
    required this.name,
    required this.address,
    required this.phone,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      name: json['name'],
      address: json['address'],
      phone: json['phone'],
    );
  }
}

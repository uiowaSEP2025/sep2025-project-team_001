class Restaurant {
  final String name;
  final String address;
  final String phone;
  final int id;

  Restaurant({
    required this.id,
    required this.name,
    required this.address,
    required this.phone,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      address: json['address'],
      phone: json['phone'],
    );
  }
}

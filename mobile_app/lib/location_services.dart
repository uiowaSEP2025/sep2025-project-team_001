import 'dart:convert';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;

Future<Position?> getCurrentLocation() async {
  bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
  if (!serviceEnabled) {
    await Geolocator.openLocationSettings();
    return null;
  }

  LocationPermission permission = await Geolocator.checkPermission();
  if (permission == LocationPermission.denied) {
    permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.deniedForever ||
        permission == LocationPermission.denied) {
      return null;
    }
  }

  return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high);
}

Future<bool> isInsideRestaurant(
    Position userPosition, String restaurantAddress) async {
  final restaurantLatLong = await getCoordinatesFromAddress(restaurantAddress);

  if (restaurantLatLong != null) {
    double distance = Geolocator.distanceBetween(
      userPosition.latitude,
      userPosition.longitude,
      restaurantLatLong.latitude,
      restaurantLatLong.longitude,
    );
    return distance <= 50;
  }
  return false;
}

class LatLong {
  final double latitude;
  final double longitude;

  LatLong(this.latitude, this.longitude);
}

Future<LatLong?> getCoordinatesFromAddress(String address) async {
  final apiKey = dotenv.env['GOOGLE_PLACES_API_KEY'];
  if (apiKey == null || apiKey.isEmpty) {
    throw Exception('Missing GOOGLE_PLACES_API_KEY in .env');
  }

  final encodedAddress = Uri.encodeComponent(address);
  final url =
      'https://maps.googleapis.com/maps/api/geocode/json?address=$encodedAddress&key=$apiKey';

  final response = await http.get(Uri.parse(url));

  if (response.statusCode == 200) {
    final data = json.decode(response.body);

    if (data['status'] == 'OK' && data['results'].isNotEmpty) {
      final location = data['results'][0]['geometry']['location'];
      return LatLong(location['lat'], location['lng']);
    } else {
      print(
          'Geocoding failed: ${data['status']} - ${data['error_message'] ?? 'No error message'}');
    }
  } else {
    print('HTTP error ${response.statusCode}: ${response.reasonPhrase}');
  }

  return null;
}

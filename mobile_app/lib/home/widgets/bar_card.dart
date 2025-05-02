import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';

class BarCard extends StatelessWidget {
  final Restaurant bar;
  final double screenWidth;
  final double screenHeight;

  const BarCard(
      {super.key,
      required this.bar,
      required this.screenHeight,
      required this.screenWidth});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: screenWidth * 0.41,
      height: screenWidth * 0.6,
      padding: EdgeInsets.all(screenWidth * 0.05),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.3), blurRadius: 5)
        ],
      ),
      child: Column(
        children: [
          bar.restaurantImageUrl != null
              ? Image.network(
                  bar.restaurantImageUrl!,
                  width: screenWidth * 0.28,
                  height: screenWidth * 0.27,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) => const Icon(
                    Icons.broken_image,
                    size: 40,
                    color: Colors.grey,
                  ),
                )
              : const Icon(
                  Icons.image_not_supported,
                  size: 40,
                  color: Colors.grey,
                ),
          SizedBox(
            height: screenWidth * 0.02,
          ),
          Text(bar.name,
              textAlign: TextAlign.center,
              style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black)),
        ],
      ),
    );
  }
}

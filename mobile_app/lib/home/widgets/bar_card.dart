import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/utils/base_64_image_with_fallback.dart';

class BarCard extends StatelessWidget {
  final Restaurant bar;
  final double screenWidth;
  final double screenHeight;

  const BarCard(
      {super.key,
      required this.bar,
      required this.screenHeight,
      required this.screenWidth
      });

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
              Base64ImageWithFallback(
                      width: screenWidth * 0.28,
                          height: screenWidth * 0.27,
                        base64ImageString: bar.base64image),
          SizedBox(
            height: screenWidth * 0.02,
          ),
          Text(bar.name,
              textAlign: TextAlign.center,
              style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black)),
        ],
      ),
    );
  }
}

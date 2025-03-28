import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';

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
          Image.network(
              "https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2FscoutsLogo.png?alt=media&token=512cb083-e65c-4435-ae27-018d7467473c",
              height: screenWidth * 0.27,
              fit: BoxFit.cover),
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

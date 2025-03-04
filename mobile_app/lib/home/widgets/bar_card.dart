import 'package:flutter/material.dart';
import 'package:mobile_app/design/app_colors.dart';
import 'package:mobile_app/objects/bar.dart';

class BarCard extends StatelessWidget {
  final Bar bar;
  final double screenWidth;
  final double screenHeight;
  final bool isSelected;

  const BarCard({Key? key, required this.bar, required this.screenHeight, required this.screenWidth, this.isSelected = false}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(screenWidth * 0.05),
      decoration: BoxDecoration(
        color: isSelected ? AppColors.primaryColor : Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.3), blurRadius: 5)],
      ),
      child: Column(
        children: [
          Image.network(bar.imageUrl, height: screenWidth*0.27, fit: BoxFit.cover),
          SizedBox(height: screenWidth*0.025),
          Text(bar.name, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: isSelected ? Colors.white : Colors.black)),
        ],
      ),
    );
  }
}

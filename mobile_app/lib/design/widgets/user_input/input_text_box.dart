import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';

class InputTextBox extends StatelessWidget {
  const InputTextBox(
      {super.key,
      required this.onChanged,
      required this.screenWidth,
      required this.screenHeight,
      required this.label,
      required this.hintText,
      required this.controller,
      required this.onSubmitted});

  final double screenWidth;
  final double screenHeight;
  final String label;
  final String hintText;
  final TextEditingController controller;
  final VoidCallback onSubmitted;
  final VoidCallback onChanged;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        (label != "")
            ? Row(
                children: [
                  Text(
                    label,
                    style: AppTextStyles.textFieldLabel(
                        screenHeight, AppColors.paragraphText),
                  ),
                ],
              )
            : Container(),
        Container(
          height: screenWidth * 0.12,
          child: TextField(
            onChanged: (value) {
              onChanged();
            },
            maxLines: 1,
            onSubmitted: (value) {
              onSubmitted();
            },
            controller: controller,
            cursorColor: AppColors.primaryColor,
            decoration: InputDecoration(
                contentPadding: EdgeInsets.only(left: screenWidth * 0.025),
                filled: true,
                fillColor: AppColors.whiteText,
                border: OutlineInputBorder(),
                hintText: hintText),
          ),
        ),
      ],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';

class PasswordTextBox extends StatefulWidget {
  final double screenWidth;
  final double screenHeight;
  final String label;
  final String hintText;
  final TextEditingController controller;
  final VoidCallback onSubmitted;

  const PasswordTextBox(
      {super.key,
      required this.screenWidth,
      required this.screenHeight,
      required this.label,
      required this.hintText,
      required this.controller,
      required this.onSubmitted});

  @override
  State<PasswordTextBox> createState() => _PasswordTextBoxState();
}

class _PasswordTextBoxState extends State<PasswordTextBox> {
  bool passwordVisible = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Text(
              widget.label,
              style: AppTextStyles.textFieldLabel(
                  widget.screenHeight, AppColors.paragraphText),
            ),
          ],
        ),
        SizedBox(
            height: widget.screenWidth * 0.12,
            child: TextField(
              obscureText: passwordVisible,
              decoration: InputDecoration(
                contentPadding:
                    EdgeInsets.only(left: widget.screenWidth * 0.025),
                fillColor: AppColors.whiteText,
                border: const OutlineInputBorder(),
                hintText: "Password",
                helperStyle: const TextStyle(color: AppColors.warning),
                suffixIcon: IconButton(
                  icon: Icon(passwordVisible
                      ? Icons.visibility
                      : Icons.visibility_off),
                  onPressed: () {
                    setState(
                      () {
                        passwordVisible = !passwordVisible;
                      },
                    );
                  },
                ),
                filled: true,
              ),
              keyboardType: TextInputType.visiblePassword,
              controller: widget.controller,
              textInputAction: TextInputAction.done,
            )),
      ],
    );
  }
}

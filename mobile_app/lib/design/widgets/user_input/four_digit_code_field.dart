import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';

class FourDigitCodeField extends StatefulWidget {
  final Function(String) onChanged;
  final double screenWidth;
  final double screenHeight;

  const FourDigitCodeField(
      {Key? key,
      required this.onChanged,
      required this.screenHeight,
      required this.screenWidth})
      : super(key: key);

  @override
  State<FourDigitCodeField> createState() => _FourDigitCodeFieldState();
}

class _FourDigitCodeFieldState extends State<FourDigitCodeField> {
  final List<TextEditingController> _controllers =
      List.generate(4, (index) => TextEditingController());
  final List<FocusNode> _focusNodes = List.generate(4, (index) => FocusNode());
  String code = "";

  @override
  void dispose() {
    for (var controller in _controllers) {
      controller.dispose();
    }
    for (var node in _focusNodes) {
      node.dispose();
    }
    super.dispose();
  }

  void _onChanged(String value, int index) {
    if (value.isNotEmpty && index < 3) {
      _focusNodes[index + 1].requestFocus();
    }

    String enteredCode = _controllers.map((e) => e.text).join();

    widget.onChanged(enteredCode);
  }

  void _onBackspace(String value, int index) {
    if (value.isEmpty && index > 0) {
      _focusNodes[index - 1].requestFocus();
      _controllers[index - 1].clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(4, (index) {
        return Container(
          width: widget.screenWidth * 0.12,
          height: widget.screenWidth * 0.12,
          margin: EdgeInsets.symmetric(horizontal: widget.screenWidth * 0.02),
          child: TextField(
            controller: _controllers[index],
            focusNode: _focusNodes[index],
            keyboardType: TextInputType.number,
            textAlign: TextAlign.center,
            maxLength: 1,
            style: AppTextStyles.appBarText(widget.screenHeight, Colors.black),
            cursorColor: AppColors.primaryColor,
            decoration: InputDecoration(
              contentPadding: EdgeInsets.all(0),
              counterText: "",
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: BorderSide(color: Colors.grey.shade400),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: BorderSide(color: AppColors.primaryColor, width: 2),
              ),
            ),
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
            onChanged: (value) => _onChanged(value, index),
            onSubmitted: (_) =>
                widget.onChanged(_controllers.map((e) => e.text).join()),
            onEditingComplete: () =>
                _onBackspace(_controllers[index].text, index),
          ),
        );
      }),
    );
  }
}

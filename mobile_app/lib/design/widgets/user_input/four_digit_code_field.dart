import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class FourDigitCodeField extends StatefulWidget {
  final Function(String) onCompleted;

  const FourDigitCodeField({Key? key, required this.onCompleted})
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
    if (enteredCode.length == 4) {
      widget.onCompleted(enteredCode);
    }
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
          width: 50,
          height: 50,
          margin: EdgeInsets.symmetric(horizontal: 5),
          child: TextField(
            controller: _controllers[index],
            focusNode: _focusNodes[index],
            keyboardType: TextInputType.number,
            textAlign: TextAlign.center,
            maxLength: 1,
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            cursorColor: Colors.blue,
            decoration: InputDecoration(
              counterText: "",
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: BorderSide(color: Colors.grey.shade400),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: BorderSide(color: Colors.blue, width: 2),
              ),
            ),
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
            onChanged: (value) => _onChanged(value, index),
            onSubmitted: (_) =>
                widget.onCompleted(_controllers.map((e) => e.text).join()),
            onEditingComplete: () =>
                _onBackspace(_controllers[index].text, index),
          ),
        );
      }),
    );
  }
}

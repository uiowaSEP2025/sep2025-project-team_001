import 'package:flutter/cupertino.dart';

class EnterNewPassword extends StatefulWidget {
final VoidCallback onNext;

  const EnterNewPassword({super.key, required this.onNext});

  @override
  State<EnterNewPassword> createState() => _EnterNewPasswordState();
}

class _EnterNewPasswordState extends State<EnterNewPassword> {
  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}
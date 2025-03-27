import 'package:flutter/material.dart';

class SearchBox extends StatelessWidget {
  final String hintText;
  final Function(String) onChanged;
  final double screenHeight;

  const SearchBox({
    super.key,
    required this.onChanged,
    this.hintText = "Search...",
    required this.screenHeight,

  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: screenHeight*0.1,
      child: TextField(
        onChanged: onChanged,
        decoration: InputDecoration(
          hintText: hintText,
          prefixIcon: const Icon(Icons.search),
          filled: true,
          fillColor: Colors.grey[100],
          contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 12),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
        ),
      ),
    );
  }
}

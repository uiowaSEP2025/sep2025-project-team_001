import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class Base64ImageWithFallback extends StatelessWidget {
  final String? base64ImageString;
  final double height; 
  final double width;

  const Base64ImageWithFallback({super.key, required this.base64ImageString, required this.height, required this.width});

  @override
  Widget build(BuildContext context) {
    if(this.base64ImageString == null){
       return const Icon(Icons.broken_image, size: 40, color: Colors.grey);
    }
    else{
 try {
      final base64String = base64ImageString!.split(',').last;
      Uint8List imageBytes = base64Decode(base64String);

      return Image.memory(
        height: height,
        width: width,
        imageBytes,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) {
          return const Icon(Icons.broken_image, size: 40, color: Colors.grey);
        },
      );
    } catch (e) {
      return const Icon(Icons.broken_image, size: 40, color: Colors.grey);
    }
    }
   
  }
}

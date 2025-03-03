import 'package:flutter/material.dart';
import 'package:mobile_app/objects/bar.dart';

class BarCard extends StatelessWidget {
  final Bar bar;

  const BarCard({Key? key, required this.bar}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(5.0),
      padding: const EdgeInsets.all(10.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.3), blurRadius: 5)],
      ),
      child: Column(
        children: [
          Image.network(bar.imageUrl, height: 80, fit: BoxFit.cover),
          const SizedBox(height: 10),
          Text(bar.name, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
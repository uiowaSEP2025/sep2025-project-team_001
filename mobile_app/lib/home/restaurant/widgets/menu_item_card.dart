import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/classes/menu_item.dart';

class MenuItemCard extends StatelessWidget {
final MenuItem item; 
final double screenHeight;
final double screenWidth;
final double horizontalSpacing;
final double verticalSpacing;

  const MenuItemCard({super.key, required this.item, required this.screenHeight, required this.screenWidth, required this.horizontalSpacing, required this.verticalSpacing});

  @override
  Widget build(BuildContext context) {
    return Padding(
  padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
  child: Card(
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    elevation: 3,
    child: Padding(
      padding: const EdgeInsets.all(12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              'https://firebasestorage.googleapis.com/v0/b/mi-cielo-app.appspot.com/o/tests%2Fdrink.jpg?alt=media&token=5704bdff-9b69-4594-8c97-aa4e88025ef6', //todo use actual images for each of the menu items
              width: screenWidth*0.25,
              height: screenWidth*0.30,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(width: 12),
          // 📋 Info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.name, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text(
                  item.description,
                  style: TextStyle(color: Colors.grey[600]),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('\$${item.price.toStringAsFixed(2)}',
                        style: TextStyle(fontWeight: FontWeight.w600)),
                    item.available
                        ? ElevatedButton(
                            onPressed: () {
                              // Add to cart
                            },
                            child: Text("Add"),
                            style: ElevatedButton.styleFrom(
                              padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                              textStyle: TextStyle(fontSize: 12),
                            ),
                          )
                        : Text("Unavailable", style: TextStyle(color: Colors.red)),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  ),
);
  }
}
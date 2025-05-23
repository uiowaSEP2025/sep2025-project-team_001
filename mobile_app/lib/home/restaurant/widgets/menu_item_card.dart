import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';

class MenuItemCard extends StatelessWidget {
  final MenuItem item;
  final double screenHeight;
  final double screenWidth;
  final double horizontalSpacing;
  final double verticalSpacing;
  final Function(MenuItem) onAddToCart;

  const MenuItemCard(
      {super.key,
      required this.item,
      required this.screenHeight,
      required this.screenWidth,
      required this.horizontalSpacing,
      required this.verticalSpacing,
      required this.onAddToCart});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
      child: Card(
        color: AppColors.secondary,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        elevation: 3,
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: SizedBox(
            height: screenWidth * 0.32,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: item.itemImageUrl != null
                      ? Image.network(
                          item.itemImageUrl!,
                          width: screenWidth * 0.28,
                          height: screenWidth * 0.32,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) =>
                              const Icon(
                            Icons.broken_image,
                            size: 40,
                            color: Colors.grey,
                          ),
                        )
                      : const Icon(
                          Icons.image_not_supported,
                          size: 40,
                          color: Colors.grey,
                        ),
                ),
                SizedBox(width: horizontalSpacing),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(item.name,
                          style: AppTextStyles.buttonText(
                              screenHeight, Colors.black)),
                      const SizedBox(height: 4),
                      Text(
                        item.description,
                        style: AppTextStyles.subtitleParagraph(
                            screenHeight * 0.85, AppColors.paragraphText),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const Spacer(),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text('\$${item.price.toStringAsFixed(2)}',
                              style:
                                  const TextStyle(fontWeight: FontWeight.w600)),
                          item.available
                              ? ElevatedButton(
                                  onPressed: () => onAddToCart(item),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppColors.primaryColor,
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: 16, vertical: 10),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                    textStyle: AppTextStyles.buttonText(
                                        screenHeight * 0.8,
                                        AppColors.whiteText),
                                  ),
                                  child: const Text("Add to Cart"),
                                )
                              : const Text("Unavailable",
                                  style: TextStyle(color: Colors.red)),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

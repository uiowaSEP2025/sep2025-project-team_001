import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';
import 'package:mobile_app/home/restaurant/services/api_services.dart';
import 'package:mobile_app/home/restaurant/widgets/menu_item_card.dart';
import 'package:mobile_app/utils/base_64_image_with_fallback.dart';

class RestaurantMenuScreen extends StatefulWidget {
  final Restaurant restaurant;
  const RestaurantMenuScreen({super.key, required this.restaurant});

  @override
  State<RestaurantMenuScreen> createState() => _RestaurantMenuScreenState();
}

class _RestaurantMenuScreenState extends State<RestaurantMenuScreen> {
  bool isLoading = true;
  bool errorFetching = false;
  List<MenuItem> items = [];
  String selectedCategory = 'All';
  late int restaurantId;
  Map<String, CartItem> cart = {};

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    restaurantId = args['restaurant'].id;
    _fetchMenuItems();
  }

  Future<void> _fetchMenuItems() async {
    try {
      setState(() {
        isLoading = true;
        errorFetching = false;
      });

      items = await fetchMenuItems(restaurantId);

      setState(() {
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        print(e);
        isLoading = false;
        errorFetching = true;
      });
    }
  }

  void _addToCart(MenuItem item) {
    setState(() {
      if (cart.containsKey(item.name)) {
        cart[item.name]!.quantity += 1;
      } else {
        cart[item.name] = CartItem(item: item);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    if (isLoading) {
      return Scaffold(
        appBar: AppBar(
            title: Text("Menu",
                style: AppTextStyles.appBarText(screenHeight, Colors.black))),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (errorFetching) {
      return Scaffold(
        appBar: AppBar(
            title: Text("Menu",
                style: AppTextStyles.appBarText(screenHeight, Colors.black))),
        body: const Center(child: Text("Failed to load menu")),
      );
    }

    final categories = [
      'All',
      ...{for (var item in items) item.category}
    ];
    final filteredItems = (selectedCategory == 'All')
        ? items
        : items.where((item) => item.category == selectedCategory).toList();

    return Scaffold(
      appBar: AppBar(
          title: Text("Menu",
              style: AppTextStyles.appBarText(screenHeight, Colors.black))),
      body: Column(
        children: [
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: categories.map((cat) {
                return Padding(
                  padding: EdgeInsets.only(
                      left: horizontalSpacing / 2,
                      right: horizontalSpacing / 2,
                      top: verticalSpacing / 2),
                  child: ChoiceChip(
                    label: Text(cat),
                    selected: selectedCategory == cat,
                    onSelected: (_) {
                      setState(() => selectedCategory = cat);
                    },
                  ),
                );
              }).toList(),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filteredItems.length,
              itemBuilder: (context, index) {
                final item = filteredItems[index];
                return GestureDetector(
                  onTap: () {
                    final base64String = item.base64image!.split(',').last;
                    Uint8List imageBytes = base64Decode(base64String);
                    _openItemModal(context, item, screenHeight, screenWidth,
                        imageBytes, verticalSpacing, horizontalSpacing);
                  },
                  child: MenuItemCard(
                    item: item,
                    screenHeight: screenHeight,
                    screenWidth: screenWidth,
                    horizontalSpacing: horizontalSpacing,
                    verticalSpacing: verticalSpacing,
                    onAddToCart: (menuItem) {
                      final base64String =
                          menuItem.base64image!.split(',').last;
                      Uint8List imageBytes = base64Decode(base64String);
                      _openItemModal(context, item, screenHeight, screenWidth,
                          imageBytes, verticalSpacing, horizontalSpacing);
                    },
                  ),
                );
              },
            ),
          ),
          SizedBox(
            height: verticalSpacing * 2,
          )
        ],
      ),
      floatingActionButton: cart.isNotEmpty
          ? SizedBox(
              height: screenWidth * 0.12,
              width: screenWidth - horizontalSpacing * 2,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                onPressed: () async {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => CartScreen(
                        cart: cart,
                        restaurant: widget.restaurant,
                        onCartUpdated: (updatedCart) {
                          setState(() {
                            cart = updatedCart;
                          });
                        },
                      ),
                    ),
                  );
                },
                icon: const Icon(Icons.shopping_cart, color: Colors.white),
                label: Text(
                  "Cart (${cart.values.fold<int>(0, (sum, item) => sum + item.quantity)})",
                  style: AppTextStyles.buttonText(
                      screenHeight, AppColors.whiteText),
                ),
              ),
            )
          : null,
    );
  }

  Future<void> _openItemModal(
      BuildContext context,
      MenuItem item,
      double screenHeight,
      double screenWidth,
      Uint8List imageBytes,
      double verticalSpacing,
      double horizontalSpacing) {
    return showModalBottomSheet<void>(
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(40)),
        ),
        isScrollControlled: true,
        context: context,
        builder: (BuildContext context) {
          List<bool> ingredientSelections =
              List.generate(item.ingredients.length, (_) => true);

          bool expandDescription = false;
          return StatefulBuilder(builder: (context, setState) {
            return ClipRRect(
              borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(40)),
              child: Container(
                color: Colors.white,
                height: screenHeight,
                width: screenWidth,
                child: Stack(children: [
                  Positioned(
                    top: 0,
                    left: 0,
                    right: 0,
                    child: ClipRRect(
                      borderRadius:
                          const BorderRadius.vertical(top: Radius.circular(30)),
                      child: SizedBox(
                        height: screenHeight * 0.4,
                        child: Image.memory(
                          imageBytes,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) {
                            return const Icon(Icons.broken_image,
                                size: 40, color: Colors.grey);
                          },
                        ),
                      ),
                    ),
                  ),
                  Positioned.fill(
                    child: SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(
                            height: screenHeight * 0.4,
                          ),
                          Container(
                            padding: EdgeInsets.only(
                                top: verticalSpacing * .5,
                                left: horizontalSpacing,
                                right: horizontalSpacing),
                            color: Colors.white,
                            child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    item.name,
                                    textAlign: TextAlign.left,
                                    style: AppTextStyles.bigBoldLetters(
                                        screenHeight * 0.7, Colors.black),
                                  ),
                                  SizedBox(
                                    height: verticalSpacing * 0.5,
                                  ),
                                  GestureDetector(
                                    onTap: () {
                                      setState(() {
                                        expandDescription = !expandDescription;
                                      });
                                    },
                                    child: Text(
                                      item.description,
                                      textAlign: TextAlign.left,
                                      maxLines: expandDescription ? null : 4,
                                      overflow: expandDescription
                                          ? TextOverflow.visible
                                          : TextOverflow.ellipsis,
                                      style: AppTextStyles.subtitleParagraph(
                                          screenHeight,
                                          AppColors.paragraphText),
                                    ),
                                  ),
                                  SizedBox(
                                    height: verticalSpacing * 0.5,
                                  ),
                                  Text("Ingredients:",
                                      style: AppTextStyles.buttonText(
                                          screenHeight,
                                          AppColors.paragraphText)),
                                  ...List.generate(item.ingredients.length,
                                      (index) {
                                    final ingredient = item.ingredients[index];
                                    return CheckboxListTile(
                                      title: Text(ingredient.name),
                                      value: ingredientSelections[index],
                                      onChanged: (value) {
                                        setState(() {
                                          ingredientSelections[index] = value!;
                                        });
                                      },
                                    );
                                  }),
                                  SizedBox(
                                    height: verticalSpacing,
                                  )
                                ]),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Positioned(
                    bottom: 24,
                    left: 24,
                    right: 24,
                    child: SizedBox(
                      height: screenWidth * 0.12,
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryColor,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        onPressed: () {
                          Navigator.of(context).pop();
                          _addToCart(item);
                        },
                        icon: const Icon(Icons.add_shopping_cart,
                            color: Colors.white),
                        label: Text(
                          "Add to Cart",
                          style: AppTextStyles.buttonText(
                              screenHeight, Colors.white),
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    top: 60,
                    right: 16,
                    child: GestureDetector(
                      onTap: () => Navigator.of(context).pop(),
                      child: Container(
                        width: screenWidth * 0.1,
                        height: screenWidth * 0.1,
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.5),
                          shape: BoxShape.circle,
                        ),
                        child: const Center(
                          child:
                              Icon(Icons.close, color: Colors.white, size: 20),
                        ),
                      ),
                    ),
                  ),
                ]),
              ),
            );
          });
        });
  }
}

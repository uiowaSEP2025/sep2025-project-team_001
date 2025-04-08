import 'package:flutter/material.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';
import 'package:mobile_app/home/restaurant/services/api_services.dart';
import 'package:mobile_app/home/restaurant/widgets/menu_item_card.dart';

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
                return MenuItemCard(
                  item: item,
                  screenHeight: screenHeight,
                  screenWidth: screenWidth,
                  horizontalSpacing: horizontalSpacing,
                  verticalSpacing: verticalSpacing,
                  onAddToCart: _addToCart,
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
}

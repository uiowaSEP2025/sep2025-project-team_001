import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/models/menu_item.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
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

  String _generateCartKey(MenuItem item, List<int> unwantedIngredientIds) {
    final sortedIds = List.from(unwantedIngredientIds)..sort();
    return '${item.id}_${sortedIds.join("_")}';
  }

  void _addToCart(MenuItem item, List<int> unwantedIngredientsIds,
      List<String> unwantedIngredientsNames) {
    final key = _generateCartKey(item, unwantedIngredientsIds);

    setState(() {
      if (cart.containsKey(key)) {
        cart[key]!.quantity += 1;
      } else {
        cart[key] = CartItem(
            item: item,
            unwantedIngredientsIds: unwantedIngredientsIds,
            unwantedIngredientNames: unwantedIngredientsNames);
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
                    _openItemModalWithUrl(context, item, screenHeight,
                        screenWidth, verticalSpacing, horizontalSpacing);
                  },
                  child: MenuItemCard(
                    item: item,
                    screenHeight: screenHeight,
                    screenWidth: screenWidth,
                    horizontalSpacing: horizontalSpacing,
                    verticalSpacing: verticalSpacing,
                    onAddToCart: (menuItem) {
                      _openItemModalWithUrl(context, menuItem, screenHeight,
                          screenWidth, verticalSpacing, horizontalSpacing);
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

  Future<void> _openItemModalWithUrl(
    BuildContext context,
    MenuItem item,
    double screenHeight,
    double screenWidth,
    double verticalSpacing,
    double horizontalSpacing,
  ) {
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
            borderRadius: const BorderRadius.vertical(top: Radius.circular(40)),
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
                      child: item.itemImageUrl != null
                          ? Image.network(
                              item.itemImageUrl!,
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) =>
                                  const Icon(Icons.broken_image,
                                      size: 40, color: Colors.grey),
                            )
                          : const Icon(Icons.image_not_supported,
                              size: 40, color: Colors.grey),
                    ),
                  ),
                ),
                // keep the rest of the UI the same
                // ...
              ]),
            ),
          );
        });
      },
    );
  }
}

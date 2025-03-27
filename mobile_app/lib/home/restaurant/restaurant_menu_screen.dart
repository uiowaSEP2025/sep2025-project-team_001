import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/classes/menu_item.dart';
import 'package:mobile_app/home/restaurant/cart_screen.dart';
import 'package:mobile_app/home/restaurant/models/cart_item.dart';
import 'package:mobile_app/home/restaurant/services/api_services.dart';
import 'package:mobile_app/home/restaurant/widgets/menu_item_card.dart';

class RestaurantMenuScreen extends StatefulWidget {
  final String restaurantName;
  const RestaurantMenuScreen({super.key, required this.restaurantName});

  @override
  State<RestaurantMenuScreen> createState() => _RestaurantMenuScreenState();
}

class _RestaurantMenuScreenState extends State<RestaurantMenuScreen> {
bool isLoading = true;
  bool errorFetching = false;
  List<MenuItem> items = [];
  String selectedCategory = 'All';
  late String restaurantName;
  Map<String , CartItem> cart = {};

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)!.settings.arguments as Map;
    restaurantName = args['restaurant'];
    _fetchMenuItems();
  }

  Future<void> _fetchMenuItems() async {
    try {
      setState(() {
        isLoading = true;
        errorFetching = false;
      });

      items = await fetchMenuItems(restaurantName);

      setState(() {
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
        errorFetching = true;
      });
    }
  }

  void  _addToCart(MenuItem item) {
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
        appBar: AppBar(title: Text("Menu")),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (errorFetching) {
      return Scaffold(
        appBar: AppBar(title: Text("Menu")),
        body: Center(child: Text("Failed to load menu")),
      );
    }

    final categories = ['All', ...{for (var item in items) item.category}];
    final filteredItems = (selectedCategory == 'All')
        ? items
        : items.where((item) => item.category == selectedCategory).toList();

    return Scaffold(
      appBar: AppBar(title: Text("Menu")),
      body: Column(
        children: [
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: categories.map((cat) {
                return Padding(
                  padding: EdgeInsets.only(left:horizontalSpacing/2,right: horizontalSpacing/2, top: verticalSpacing/2),
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
                return MenuItemCard(item: item, screenHeight: screenHeight, screenWidth: screenWidth, horizontalSpacing: horizontalSpacing, verticalSpacing: verticalSpacing, onAddToCart: _addToCart,);
              },
            ),
          ),
        ],
      ),
      floatingActionButton: cart.isNotEmpty
    ? FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => CartScreen(cart: cart),
            ),
          );
        },
        label: Text('Cart (${cart.values.fold<int>(0, (sum, item) => sum + item.quantity)})'),
        icon: Icon(Icons.shopping_cart),
      )
    : null,

    );
  }
}
import 'package:mobile_app/home/restaurant/models/menu_item.dart';

class CartItem {
  final MenuItem item;
  int quantity;
  List<int> unwantedIngredientsIds;
  List<String> unwantedIngredientNames;


  CartItem({required this.item, this.quantity = 1, this.unwantedIngredientsIds = const [], this.unwantedIngredientNames = const []});

  Map<String, dynamic> toJson(){
    return {
       'item_id': item.id,
      'quantity': quantity,
      'unwanted_ingredients_ids': unwantedIngredientsIds,
      'unwanted_ingredients_names' : unwantedIngredientNames
    };
  }
}

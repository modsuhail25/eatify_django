from django.shortcuts import render
from .models import Restaurant,FoodItem,Category
from order.models import CartItem,Cart

def restaurant_detail(request,**kwargs):
    print(kwargs)
    restaurant_id = kwargs.get("restaurant_id")
    restaurant = Restaurant.objects.get(id=restaurant_id)
    categories = Category.objects.filter(restaurant=restaurant).prefetch_related("food_items")
    cart_dict = []
   
    print("requess",request.user.is_authenticated)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user) 
        cart_items = CartItem.objects.filter(cart=cart).select_related("food_item")
        cart_food_ids = set(cart_items.values_list("food_item_id", flat=True))
        cart_dict = {str(item.food_item.id):item.quantity  for item in cart_items}

        for category in categories:
            for food in category.food_items.all():
                food.in_cart = food.id in cart_food_ids
    print("cart",cart_dict)
    data = {
        "restaurant":restaurant,
        "categories":categories,
        "cart_dict":cart_dict
    }
        
    
    print(restaurant)
    return render(request,'restaurant_detail.html',data)

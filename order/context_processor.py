from users.models import User

def cart_item_count(request):
    item_count = 0
    if request.user.is_authenticated:
        user = request.user
        if user.role == User.CUSTOMER:
            cart = user.cart
            cart_item_count = cart.cart_items.all().count()
            item_count = cart_item_count
    return {"cart_item_count":item_count}

def get_restaurant_name(request):
    user = request.user
    restaurant_name =""
    if request.user.is_authenticated:
        if user.role == User.VENDOR:
            try:
                restaurant = user.restaurant
                restaurant_name = restaurant.name
            except :
                restaurant_name = ""
    return {"restaurant_name":restaurant_name}
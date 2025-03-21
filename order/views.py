from django.shortcuts import render
from .models import Cart,CartItem
from vendor.models import FoodItem
from django.http import JsonResponse
import json


def add_to_cart(request):

    if request.method == "POST":
        print("req",request.body)
        data = json.loads(request.body)
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
            except:
                cart = Cart.objects.create(user=request.user)

            food_item_id = data.get("product_id",None)
            item = cart.add_food_item(food_item_id)
            data = {
                "message":"Item added to cart",
                "quantity":item.quantity
            }
            return JsonResponse(data,status=200)
        
        else:
            return JsonResponse({"message":"user not authenticated"},status=400)
             
            # product_id = int(data.get("product_id"))

            # try:
            #     food_item = FoodItem.objects.get(id=product_id)
            # except FoodItem.DoesNotExist:
            #     return JsonResponse({"error": "Food item not found"}, status=404)

            # restaurant_id = food_item.restaurant.id
            # session = request.session

            # if "cart" not in session:
            #     session["cart"] = {"fooditems": {}}

            # cart = session["cart"]
            # session_fooditems = cart["fooditems"]

            # if "restaurant_id" in cart:
            #     cart_restaurant_id = cart.get("restaurant_id")
            #     if cart_restaurant_id != restaurant_id:
            #         return JsonResponse({"error": "Can't add food from another restaurant"}, status=400)

            # if "restaurant_id" not in cart:
            #     cart["restaurant_id"] = restaurant_id

            # product_id_str = str(product_id)

            # if product_id_str in session_fooditems:
            #     session_fooditems[product_id_str] += 1
            # else:
            #     session_fooditems[product_id_str] = 1

            # session.modified = True 

            # print("sesso=",request.session["cart"])
            
            # return JsonResponse({"message":"Item added to cart"})

def view_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        data = {
            "cart_items":cart_items
        }
    return render(request,"cart.html",data)



            


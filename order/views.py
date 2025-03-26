from django.shortcuts import render,redirect
from .models import Cart,CartItem,Address,Order
from vendor.models import FoodItem
from django.http import JsonResponse
import sweetify
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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

def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        food_id = data.get("product_id")
        cart = Cart.objects.get(user=request.user)
        action = data.get("action")
        if action == "increase":
            cart_item = cart.add_food_item(food_id)
            data = {"quantity":cart_item.quantity,
                    "total_price":cart_item.get_total}
            return JsonResponse(data,status=200)
        elif action == "decrease":
            cart.decrease_food_item(food_id)
        elif action == "remove":
            cart.remove_food_item(food_id)
        
        
        return JsonResponse({"message":"Item added to cart"},status=200)
    
def remove_food_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        food_id = data.get("product_id")
        cart = Cart.objects.get(user=request.user)
        cart.remove_food_item(food_id)
        return JsonResponse({"message":"Item added to cart"},status=200)
        


@login_required(login_url="/user/customer/signin")
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = []
        try:
            cart = Cart.objects.get(user = request.user)
            cart_items = CartItem.objects.filter(cart=cart).order_by("-id")
        except:
            pass
        data = {
            "cart_items":cart_items,
            "cart":cart
        }
    return render(request,"cart.html",data)


def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        data = {
            "cart_items":cart_items,
            "cart":cart
        }
    return render(request,'checkout.html',data)

def place_order(request):
    print("requessttt",request.method)
    if request.method == "POST":
        data = request.POST
        print("d",data)
        customer_name = data.get("customer_name")
        address = data.get("address")
        city = data.get("town")
        pincode = data.get("pincode")
        mobile_number = data.get("mobile")
        address = Address.objects.create(
            customer_name=customer_name,
            address=address,
            city = city,
            pincode=pincode,
            mobile_number=mobile_number,
            user=request.user
        )

        cart = Cart.objects.get(user=request.user)
        cart.place_order(address=address)
        sweetify.success(request,"Order placed successfully")
        return redirect("/")

    
def view_order(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(orderd_by=request.user).prefetch_related("orderitem_set").all().order_by("-id")
        data = {
            "orders":orders
        }
        return render(request,"orders.html",data)
    

@csrf_exempt  # Use this only if you don’t want to include CSRF token
def update_order_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        print("status",new_status)
        try:
            order = Order.objects.get(order_id=order_id)
            print("order",order)
            order.order_status = new_status
            order.save()
            return JsonResponse({"success": True, "message": "Status updated successfully!"})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)










            


from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
import sweetify
from users.models import User
from order.models import Order,OrderItem
from vendor.forms import VendorForm
from vendor.models import Cusines,Restaurant,FoodItem,Category




def admin_dashboard(request):
    print(request.user)
    if request.user.role == User.VENDOR:
        restaurant = request.user.restaurant
        orders = Order.objects.filter(order_restaurant=restaurant).prefetch_related("orderitem_set").all()
        print("order",orders)
        data = {"orders":orders}
    return render(request,"admin/dashboard.html",data)

def admin_signin(request):
    if request.method == "POST":
        print("req",request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,username=email,password=password)

        if user:
            if user.role == User.VENDOR:
                restaurant = user.restaurant
                if not restaurant.is_verfied:
                    sweetify.error(request,"Restaurant Not verified")
                    return redirect('vendor-signin')
                login(request,user)
                sweetify.success(request,"Login Succesfull")
                return redirect("admin-dashboard")
            else:
                sweetify.error(request,"Don't have the permission")
                redirect('vendor-signin')

        
        else:
            sweetify.error(request,'Incorrect password or Email')
            return redirect("vendor-signin")

    return render(request, "admin/signin.html")

def vendor_signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(email=email).exists():
            sweetify.error(request,"Email already exist")
            return redirect("admin-signup")


        if password != confirm_password:
            sweetify.error(request,'Incorrect password or Email')
            return redirect("vendor-signup")
        
        user = User.objects.create_user(email=email,password=password,role = User.VENDOR)
        login(request,user)
        sweetify.success(request, 'Account created')
        return redirect("vendor-register")
    return render(request,"admin/signup.html")


def vendor_register(request):
    cusines = Cusines.objects.all()
    print("cusines",cusines)
    if request.method == "POST":
        print(request.POST)
        form = VendorForm(request.POST, request.FILES)
        restaurant_name = request.POST.get("name")
        address = request.POST.get("address")
        phone_number  = request.POST.get("phone_number")
        restaurant_type = request.POST.get("type")
        profile_pic = request.FILES.get("profile_pic")
        banner_image1 = request.FILES.get("banner_image1")
        banner_image2 = request.FILES.get("banner_image2")
        banner_image3 = request.FILES.get("banner_image3")
        banner_image4 = request.FILES.get("banner_image4")
        cusine_id = request.POST.getlist("cusines")
        description = request.POST.get("description")
        location = request.POST.get("location")

        user = request.user
        restaurant = Restaurant.objects.create(user=user,name=restaurant_name,address=address,phone_number=phone_number,
            type=restaurant_type,profile_pic=profile_pic,banner_image1=banner_image1,banner_image2=banner_image2,
            banner_image3=banner_image3,banner_image4=banner_image4,description=description,location=location)
        
        for id in cusine_id:
            cusine = Cusines.objects.get(id=id)
            restaurant.cusines.add(cusine)
        sweetify.success(request,"Restaurant Registered Wait for the registration")
        return redirect("vendor-signin")
        
    form = VendorForm()
    data ={
        "cusines":cusines
    }

    return render(request,"admin/register.html",data)

def vendor_logout(request):
    logout(request)
    sweetify.success(request, 'Successfuly logout')
    return redirect("vendor-signin")


def get_food_items(request):
    restaurant = request.user.restaurant
    food_items = FoodItem.objects.filter(restaurant=restaurant)
    data = {
        "food_items":food_items
    }

    return render(request,"admin/fooditems.html",data)

def get_food_detail(request,**kwargs):
    restaurant = request.user.restaurant
    food_id = kwargs.get("food_id")
    food_item = FoodItem.objects.get(id=food_id)
    categories = Category.objects.filter(restaurant=restaurant)
    data = {
        "food_item":food_item,
        "categories":categories
    }
    if request.method == "POST":
        print(request.POST,"is_available" in request.POST)
        food_item.name = request.POST.get("food_name",food_item.name)
        food_item.discription = request.POST.get("discription",food_item.discription)
        food_item.is_available = True if "is_available" in request.POST else False
        food_item.price_per_plate = request.POST.get("price_per_plate",food_item.price_per_plate)
        category = Category.objects.get(id= request.POST.get("category_id"))
        food_item.category = category
        if request.FILES:
            print("files",request.FILES.get("food_item_image"))
            food_item.image = request.FILES.get("food_item_image")
        food_item.save()
        sweetify.success(request,"Food Item Updated")
        return redirect("vendor_food_items")

    return render(request,"admin/fooddetail.html",data)


def add_food_item(request):
    categories = Category.objects.filter(restaurant=request.user.restaurant)
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("food_name")
        discription = request.POST.get("discription")
        is_available = True if "is_available" in request.POST else False
        price_per_plate = request.POST.get("price_per_plate")
        category = Category.objects.get(id= request.POST.get("category_id"))
        image = request.FILES.get("food_item_image")
        FoodItem.objects.create(restaurant=request.user.restaurant,name=name,discription=discription,is_available=is_available,
            price_per_plate=price_per_plate,image=image,category=category)
        sweetify.success(request,"Food Item Created")
        return redirect("vendor_food_items")
    
    data ={
        "categories":categories
    }

    return render(request,"admin/addfooditem.html",data)



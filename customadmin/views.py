from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
import sweetify
from users.models import User
from order.models import Order,OrderItem
from vendor.forms import VendorForm
from vendor.models import Cusines,Restaurant




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
                login(request,user)
                sweetify.success(request,"Login Succesfull")
                return redirect("admin-dashboard")
            else:
                sweetify.error(request,"Don't have the permission")
                redirect('admin-signin')

        
        else:
            sweetify.error(request,'Incorrect password or Email')
            return redirect("admin-signin")

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
            return redirect("admin-signup")
        
        user = User.objects.create_user(email=email,password=password,role = User.CUSTOMER)
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

        user = request.user
        restaurant = Restaurant.objects.create(user=user,name=restaurant_name,address=address,phone_number=phone_number,
            type=restaurant_type,profile_pic=profile_pic,banner_image1=banner_image1,banner_image2=banner_image2,
            banner_image3=banner_image3,banner_image4=banner_image4)
        print("c",cusine_id)
        if form.is_valid():
            print("valid")
        else:
            print("Invalid")

        print(profile_pic,banner_image1,banner_image2,banner_image3,banner_image4)
        
    form = VendorForm()
    data ={
        "cusines":cusines
    }

    return render(request,"admin/register.html",data)
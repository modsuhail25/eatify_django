from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
import sweetify
from users.models import User
from order.models import Order,OrderItem




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

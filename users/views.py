from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Customer
import sweetify
from django.contrib.auth import login, authenticate,logout

def customer_signup(request):
    if request.method == "POST":
        print("reqq")
        request_data = request.POST
        email = request_data.get("email")
        password = request_data.get("password")
        confirm_password = request_data.get("confirm_password")
        profile_name = request_data.get("profile_name")
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'email already exists')
            return redirect("customer-signup")


        if password != confirm_password:
            messages.error(request,'password and confirm password not password')
            return redirect("customer-signup")
        
        user = User.objects.create_user(email=email,password=password,role = User.CUSTOMER)
        customer = Customer.objects.create(user=user,profile_name = profile_name)
        sweetify.success(request, 'Cheers to new toast')
        return redirect("/")
    return render(request,"signup.html")

def customer_sigin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,username=email,password=password)

        if user:
            login(request,user)
            sweetify.success(request,"Login Succesfull")
            return redirect("/")
        
        else:
            messages.error(request,'Incorrect password or Email')
            return redirect("customer-signin")

    return render(request,"signin.html")

def customer_logout(request):
    logout(request)
    sweetify.success(request, 'Successfuly logout')
    return redirect("/")


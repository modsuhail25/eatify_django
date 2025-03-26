from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard",admin_dashboard,name="admin-dashboard"),
    path("signin",admin_signin,name="admin-signin"),
    path("signup",vendor_signup,name="vendor-signup"),
    path('register',vendor_register,name='vendor-register')
]
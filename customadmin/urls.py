from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard",admin_dashboard,name="admin-dashboard"),
    path("signin",admin_signin,name="vendor-signin"),
    path("signup",vendor_signup,name="vendor-signup"),
    path('register',vendor_register,name='vendor-register'),
    path("food",get_food_items,name="vendor_food_items"),
    path('food/detail/<int:food_id>', get_food_detail,name="food-detail"), 
    path("add/food",add_food_item,name="add-food"),
    path('vendor-logout',vendor_logout,name="vendor-logout")
]
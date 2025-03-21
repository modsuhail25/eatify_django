from django.urls import path
from .views import *

urlpatterns = [

path('add-to-cart', add_to_cart,name="add-to-cart"),
path('cart',view_cart,name="view-cart")

]
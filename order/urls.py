from django.urls import path
from .views import *

urlpatterns = [

path('add-to-cart', add_to_cart,name="add-to-cart"),
path('cart',view_cart,name="view-cart"),
path('update/cart',update_cart,name='update-cart'),
path('checkout',checkout,name="checkout"),
path('place-order',place_order,name='place-order'),
path('order',view_order,name='order'),
path("update-order-status/", update_order_status, name="update_order_status"),
]
from django.urls import path
from .views import *

urlpatterns = [

path('detail/<int:restaurant_id>', restaurant_detail,name="restaurant-detail"),
path('',restaurants,name='restaurants')

]
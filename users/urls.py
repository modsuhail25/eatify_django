from django.urls import path
from .views import *

urlpatterns = [

path('customer/signup', customer_signup,name="customer-signup"),
path('customer/signin',customer_sigin,name="customer-signin"),
path('customer/logout',customer_logout,name="customer-logout")

]
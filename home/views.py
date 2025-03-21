from django.shortcuts import render
from vendor.models import Restaurant

def index(request):
    restaurants = Restaurant.objects.filter(is_verfied=True)
    data = {"restaurants": restaurants}
    return render(request,'home.html',data)
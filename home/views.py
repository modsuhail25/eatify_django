from django.shortcuts import render
from vendor.models import Restaurant
from django.http import JsonResponse

def index(request):
    restaurants = Restaurant.objects.filter(is_verfied=True)
    data = {"restaurants": restaurants}
    return render(request, 'home.html', data)

def search_restaurants(request):
    query = request.GET.get('query', '')
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)  # Adjust field name as necessary
        results = [{'name': restaurant.name} for restaurant in restaurants]
    else:
        results = []
    return JsonResponse(results, safe=False)
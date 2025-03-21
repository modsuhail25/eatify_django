from django.contrib import admin
from .models import Cusines,Restaurant,FoodItem,Category
from leaflet.admin import LeafletGeoAdmin

class RestaurantAdmin(LeafletGeoAdmin):
    pass

class FoodItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cusines)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(Category)

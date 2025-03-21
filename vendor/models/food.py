from .restaurant import Restaurant
from .categories import Category
from django.db import models

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="food_items")
    name = models.CharField(max_length=100)
    discription = models.TextField()    
    image = models.ImageField(upload_to="fooditem/")
    price_per_plate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
from django.db import models
from .restaurant import Restaurant
from .food import FoodItem

class Offer(models.Model):
    
    FLAT = "flat"
    PERCENTAGE = "percentage"
    
    OFFER_TYPES = [
        (FLAT, 'Flat Discount'),
        (PERCENTAGE, 'Percentage Discount'),
        ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Flat or percentage discount
    discount_percentage = models.IntegerField(blank=True,null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    food_items = models.ManyToManyField(FoodItem, related_name='offers',blank=True)  # Link offers to food items
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

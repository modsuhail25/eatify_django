from .restaurant import Restaurant
from django.db import models

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"category {self.restaurant}--{self.name}"
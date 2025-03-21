from django.db import models
from vendor.models import Restaurant,FoodItem
from users.models import User

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"cart---{self.user}"
    
    def add_food_item(self,food_item_id):
        food_item = FoodItem.objects.get(id=food_item_id)
        if CartItem.objects.filter(cart=self,food_item=food_item).exists():
            cart_item = CartItem.objects.get(cart=self,food_item=food_item)
            cart_item.quantity+=1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=self,food_item=food_item)

        return cart_item
    
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    food_item = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    orderd_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_item.name
    
    @property
    def get_total(self):
        return self.quantity*self.food_item.price_per_plate

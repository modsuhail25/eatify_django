from django.db import models
from vendor.models import Restaurant,FoodItem
from users.models import User
import time
import random

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"cart---{self.user}"
    
    @property
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total =0
        for item in cart_items:
            total+=item.food_item.price_per_plate*item.quantity
        return total


    
    def add_food_item(self,food_item_id):
        food_item = FoodItem.objects.get(id=food_item_id)
        if CartItem.objects.filter(cart=self,food_item=food_item).exists():
            cart_item = CartItem.objects.get(cart=self,food_item=food_item)
            cart_item.quantity+=1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=self,food_item=food_item)

        return cart_item
    
    def decrease_food_item(self,food_item_id):
        food_item = FoodItem.objects.get(id=food_item_id)
        cart_item = CartItem.objects.get(cart=self,food_item=food_item)
        quantity = cart_item.quantity
        if quantity>1:
            cart_item.quantity -=1
            cart_item.save()
            print("decrease",cart_item.quantity)
        else:
            cart_item.delete()
    
    def remove_food_item(self,food_item_id):
        food_item = FoodItem.objects.get(id=food_item_id)
        cart_item = CartItem.objects.get(cart=self,food_item=food_item)
        cart_item.delete()

    def place_order(self,address):
        cart_items = CartItem.objects.filter(cart=self)
        timestamp = int(time.time())  
        random_num = random.randint(1000, 9999)
        order_id = f"ORD{timestamp}{random_num}"
        order = Order.objects.create(order_id=order_id,orderd_by=self.user,order_restaurant=self.restaurant,address=address)
        for item in cart_items:
            OrderItem.objects.create(order=order,product_name=item.food_item.name,quantity=item.quantity,price=item.get_total)
            item.delete()



    
    
    
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


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=60)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=10)

    def __str__(self):
        return f"address---of--{self.customer_name}"



class Order(models.Model):
    PLACED = "placed"
    ACCEPTED = "accepted"
    READY = "ready"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELED = "canceled"

    ORDER_STATUS = (
        (ACCEPTED,"Accepted"),
        (READY,"Ready"),
        (PICKED_UP,"Picked Up"),
        (DELIVERED,"Delivered"),
        (CANCELED,"Canceled")
    )
    
    order_id = models.CharField(max_length=50)
    orderd_by = models.ForeignKey(User,on_delete=models.CASCADE)
    order_restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True)
    order_status = models.CharField(max_length=30,choices=ORDER_STATUS,default=PLACED)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    ordered_on = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"order----{self.order_id}"
    
    @property
    def get_total(self):
        order_items = OrderItem.objects.filter(order=self)
        total = 0
        for item in order_items:
            total+=item.price
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity =  models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product_name

from .models import CustomerProfile
from order.models import Cart
from django.db.models. signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomerProfile)
def add_customer_cart(sender,instance,created,**kwargs):
    print("cretaeeerrr",created)
    if created:
        print("aiiiii",instance)
        Cart.objects.create(user=instance.user)
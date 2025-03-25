from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    
    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"

    USER_TYPES = (
        (ADMIN, "Admin"),
        (CUSTOMER,'Customer'),
        (VENDOR,'Vendor'),
    )

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=15,choices=USER_TYPES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer")
    profile_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.profile_name
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer_profile")
    profile_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.profile_name

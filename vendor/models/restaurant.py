from django.contrib.gis.db import models
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Cusines(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    
    VEG = "veg"
    NON_VEG = "non_veg"
    MIXED = "mixed"

    type = (
        (VEG,"Veg"),
        (NON_VEG,"Non-Veg"),
        (MIXED,"Mixed")
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="restaurant")
    name = models.CharField(max_length=100)
    location = models.PointField()
    area = models.PolygonField(null=True,blank=True)
    address = models.TextField()
    phone_number = PhoneNumberField()
    is_verfied = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to="restaurant/profile")
    banner_image1 = models.ImageField(upload_to="restaurant/banner",null=True)
    banner_image2 = models.ImageField(upload_to="restaurant/banner",null=True)
    banner_image3 = models.ImageField(upload_to="restaurant/banner",null=True)
    banner_image4 = models.ImageField(upload_to="restaurant/banner",null=True)
    type = models.CharField(max_length=20,choices=type)
    cusines = models.ManyToManyField(Cusines)

    def __str__(self):
        return self.name
    






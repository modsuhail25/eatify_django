from django.forms import ModelForm
from .models import Restaurant

class VendorForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name","description","location","address","phone_number","profile_pic",
            "banner_image1","banner_image2","banner_image3","banner_image4","type","cusines"    ]

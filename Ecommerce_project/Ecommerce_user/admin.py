from django.contrib import admin
from .models import UserProfile, Product, ProductImage, SlideShow

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(SlideShow)
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#This is a model for profiles
class UserProfile(models.Model):
    choices=(('Buyer', 'Buyer'), ('Seller', 'Seller'))
    name=models.OneToOneField (User,related_name="user_profile", on_delete=models.CASCADE)
    bio=models.CharField(max_length=255, blank=True, null=True)
    phone=models.CharField(max_length=20, blank=True, null=True)
    whatsapp_phone=models.CharField(max_length=20, blank=True, null=True)
    profile_picture=models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    role=models.CharField(max_length=6, choices=choices, default='Buyer')
    created_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name.username
        return self.get_choice_display()

#This is the product model
class Product(models.Model):
    seller=models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    status_choices=(('instock','instock'),('outstock','outstock'))
    choices=(('Fashion','Fashion'),('Phones & Tablets','Phones & Tablets'),('Home & Office','Home & Office'),('Electronics','Electronics'),('Computing','Computing'),('Heath & Beauty','Heath & Beauty'),('Groceries','Groceries'),('Sports & Fitness','Sports & Fitness'),('Baby Products','Baby Products'),('Automotive','Automotive'))
    name=models.CharField(max_length=255, blank=False, null=False)
    category=models.CharField(max_length=255, choices=choices)
    description=models.TextField(max_length=1000, blank=True, null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=10, choices=status_choices, default="instock")
    views=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" product {self.name} for {self.seller.username}"
    
#This is a product image model
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="images")
    image=models.ImageField(upload_to="product_images/")
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"images for {self.product.name}"

#This will store the images for the homepage slideshow
class SlideShow(models.Model):
    image=models.ImageField(upload_to="slideimages/")
    name=models.CharField(max_length=255, blank=True, null=True)
    description=models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name

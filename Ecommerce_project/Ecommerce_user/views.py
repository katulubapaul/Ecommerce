from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Product, ProductImage, SlideShow
from django.contrib.auth.decorators import login_required
import os

# Create your views here.

#This carries out the user login logic
def Login_View(request):
    error=None
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error="Invalid username or password!"

    return render(request, 'login.html', {'error':error})

#This carries out the user logout logic
def Logout_View(request):
        logout(request)
        return redirect('login')

#This carries out the user registration logic
def Register_View(request):
    error=None
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        username=request.POST['username']
        if password1!=password2:
             error = "Password do not match!"
        elif User.objects.filter(username=username).exists():
            error = "Username already taken!"
        elif User.objects.filter(email=email).exists():
            error = "Email already taken!"
        else:
            user=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
            login(request, user)
            return redirect('userprofile')
    return render(request, 'signup.html', {'error':error})

#This carries a logic for viewing a specific userprofile for a logined user
@login_required
def userprofile(request):
    user=request.user
    if request.method=='POST':
        name=user
        bio=request.POST['bio']
        phone=request.POST['phone']
        whatsapp_phone=request.POST['whatsapp']
        profile_picture=request.FILES.get('image')
        role=request.POST['role']
        UserProfile.objects.create(bio=bio, phone=phone, whatsapp_phone=whatsapp_phone, profile_picture=profile_picture, name=name, role=role)
        return redirect('home')

    return render(request,"userprofile.html")

#This is a userprofile change form logic
@login_required
def userprofilechange(request):
    user=request.user
    userpro=get_object_or_404(UserProfile, name=user)
    if request.method=="POST":
            name=user
            bio=request.POST.get('bio')
            phone=request.POST['phone']
            whatsapp_phone=request.POST['whatsapp']
            profile_picture=request.FILES.get('image')

            userpro.bio=bio
            userpro.phone=phone
            userpro.whatsapp_phone=whatsapp_phone
            if profile_picture and userpro.profile_picture:
                old_pic=userpro.profile_picture.path
                if os.path.exists(old_pic):
                    os.remove(old_pic)
            if profile_picture:
                userpro.profile_picture=profile_picture

            userpro.save()
   
    return render(request, 'userprofilechange.html', {'userpro':userpro})

#This runs the product upload logic by a user
@login_required
def products(request):
    if request.method=="POST":
        name=request.POST['name']
        category=request.POST['category']
        description=request.POST['description']
        price=request.POST['price']
        images=request.FILES.getlist('images')
        seller=request.user

        product=Product.objects.create(name=name, category=category, description=description, price=price, seller=seller)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return redirect("seller_dashboard")

    return render(request,'productupload.html')

#This will have to run the logic of product details, a single page for the product
@login_required
def product_details(request, id):
    product=get_object_or_404(Product, id=id)
    return render(request, "product_details.html", {'product':product})

#This view determines which dashboard it should redirect a user to based on the role
@login_required
def dashboard(request):
    user=request.user
    profile=UserProfile.objects.get(name=user)
    if profile.role=="Seller":
        return redirect("seller_dashboard")
    else:
        return redirect("buyer_dashboard")
    
#This help user to switch roles instantly, changing the dashboard from seller_dashboard to Buyer_dashboard and vice verser
@login_required
def switch(request):
    user=request.user
    profile=UserProfile.objects.get(name=user)
    if profile.role=="Seller":
        profile.role="Buyer"
        profile.save()
        return redirect('dashboard')
    else:
        profile.role="Seller"
        profile.save()
        return redirect('dashboard')
    
#Seller view which enables user to sell products and edit the profile
@login_required
def Seller_View(request):
    user=request.user
    userdetails=UserProfile.objects.get(name=user)
    products=Product.objects.prefetch_related('images')
    return render(request, 'Seller_dashboard.html', {'userdetails':userdetails, 'products':products})

#Buyer view which enable user to view and edit the profile
@login_required
def Buyer_view(request):
    user=request.user
    userdetails=UserProfile.objects.get(name=user)

    return render(request, 'Buyer_dashboard.html', {'userdetails':userdetails})

#This is where the home login will be found, all of them
def home(request):
    images=SlideShow.objects.all()
    return render(request, 'home.html', {'images':images})
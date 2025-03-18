from django.urls import path
from .views import Login_View, Register_View, Logout_View,home, switch, userprofile, userprofilechange, products, Seller_View, dashboard, Buyer_view

urlpatterns = [
    path('login/', Login_View, name="login"),
    path('register/', Register_View, name="register"),
    path('logout/', Logout_View, name="logout"),
    path('', home, name='home'),
    path('profile/', userprofile, name='userprofile'),
    path("userprofilechange/", userprofilechange, name='userprofilechange'),
    path('product_upload/', products, name="products"),
    path('seller_dashboard/', Seller_View, name="seller_dashboard"),
    path('dashboard/', dashboard, name="dashboard"),
    path('buyer_dashboard/', Buyer_view, name="buyer_dashboard"),
    path("switch_role_dashboard/", switch, name="switch")
]

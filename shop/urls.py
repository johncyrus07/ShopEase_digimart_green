from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[path('',views.home,name='home'),path('product/<uuid:pk>/',views.detail,name='detail'),path('register/',views.register,name='register'),path('login/',auth_views.LoginView.as_view(template_name='shop/login.html'),name='login'),path('logout/',auth_views.LogoutView.as_view(),name='logout'),path('cart/',views.cart,name='cart'),path('cart/add/<uuid:pk>/',views.add_to_cart,name='add_to_cart'),path('cart/update/<uuid:pk>/',views.update_cart,name='update_cart'),path('checkout/',views.checkout,name='checkout'),path('orders/',views.orders,name='orders')]

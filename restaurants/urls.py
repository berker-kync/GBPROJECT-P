from django.urls import path, include
from . import views


urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('restaurant-list/', views.RestaurantList, name='restaurant-list'),
    path('partner/', views.partner, name='partner'),
    path('adminmain/', views.adminmain, name='adminmain'),
    path('addtomenu/', views.addtomenu, name='addtomenu'),
]
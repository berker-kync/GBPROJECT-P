from django.urls import path, include
from . import views


urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('restaurant-list/', views.RestaurantList, name='restaurant-list'),
    path('partner/', views.partner, name='partner'),
    path('adminmain/', views.adminmain, name='adminmain'),
    path('addtomenu/', views.addtomenu, name='addtomenu'),
    path('stafflogin/', views.stafflogin, name='staff-login'),
    path('stafflogout/', views.stafflogout, name='staff-logout'),
    path('orders/', views.order_list, name='order-list'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
]
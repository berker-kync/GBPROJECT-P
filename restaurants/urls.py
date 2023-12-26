from django.urls import path, include
from . import views


urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('restaurant-list/<slug:province_slug>/', views.RestaurantList, name='restaurant-list'),
    path('partner/', views.partner, name='partner'),
    path('adminmain/', views.adminmain, name='adminmain'),
    path('addtomenu/', views.addtomenu, name='addtomenu'),
    path('addtomenu/<int:item_id>/', views.addtomenu, name='edit_menu_item'),
    path('stafflogin/', views.stafflogin, name='staff-login'),
    path('stafflogout/', views.stafflogout, name='staff-logout'),
    path('order-list/', views.order_list, name='order-list'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('delete-item/<int:menu_id>/', views.delete_item, name='delete-item'),
    path('toggle-visibility/<int:item_id>/', views.toggle_visibility, name='toggle-visibility'),
    path('access-denied/', views.access_denied, name='access-denied'),

]
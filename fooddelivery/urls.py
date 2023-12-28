from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= "index"),
    path('detail-restaurant', views.detailRestaurant, name="detail-restaurant"),
    path('add_to_cart/<int:menu_id>/', views.add_to_cart, name="add_to_cart"),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('order/', views.order, name="order"),
    path('confirm', views.confirmorder, name="confirm"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('termsconditions', views.termsconditions, name="termsconditions"),
    path('privacy', views.privacy, name="privacy"),
    path('leave-review/<int:order_id>/', views.review, name="review"),
    path('login', views.Login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.user_logout, name="logout"),
    path('profile', views.profile, name='profile'),
    path('restaurants', views.restaurants, name='restaurants'),
    path('restaurant/<slug:name_slug>/', views.detailRestaurant, name='detail-restaurant'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('get-food-item-details/<int:food_item_id>/', views.get_food_item_details, name='get-food-item-details'),
    path('mail-quest', views.mailquest, name='mail-quest')
]

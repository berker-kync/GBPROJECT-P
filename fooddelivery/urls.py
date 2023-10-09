from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= "index"),
    path('detail-restaurant', views.detailRestaurant, name="detail-restaurant"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('order', views.order, name="order"),
    path('confirm', views.confirmorder, name="confirm"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('termsconditions', views.termsconditions, name="termsconditions"),
    path('privacy', views.privacy, name="privacy")
]
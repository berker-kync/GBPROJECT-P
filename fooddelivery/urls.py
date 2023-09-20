from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('detail-restaurant', views.detailRestaurant, name="detail-restaurant"),
    path('deneme', views.deneme, name="deneme"),
]
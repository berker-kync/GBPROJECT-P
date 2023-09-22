from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name= "index"),
    path('detail-restaurant/', views.detailRestaurant, name="detail-restaurant"),
    path('detail-restaurant-2/', views.detailRestaurant2, name="detail-restaurant-2"),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
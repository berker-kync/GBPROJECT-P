from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve

handler404 = 'fooddelivery.views.custom_404'

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('admin/', admin.site.urls),
    path('', include('fooddelivery.urls')),
    path('', include('restaurants.urls')),

]





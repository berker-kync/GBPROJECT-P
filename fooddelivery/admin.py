from django.contrib import admin
from .models import Product, Order, Customer, Restaurant, Restaurant_Category, Menu_Category


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'shipping_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'shipping_address')




admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Restaurant)
admin.site.register(Restaurant_Category)
admin.site.register(Menu_Category)
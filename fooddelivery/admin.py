from django.contrib import admin
from .models import Adress, Product, Order, Customer, Menu_Category
from restaurants.models import Restaurant, Restaurant_Category


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'customer_email')
    list_editable = ('status',)

class AdressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'phone', 'street', 'apartment', 'door_number', 'city', 'postal_code')
    search_fields = ('customer__name', 'name', 'phone', 'street', 'apartment', 'door_number', 'city', 'postal_code')
    list_filter = ('customer__name', 'city', 'postal_code')


admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Adress)
admin.site.register(Restaurant)
admin.site.register(Restaurant_Category)
admin.site.register(Menu_Category)
admin.site.register(Menu)


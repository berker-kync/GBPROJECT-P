from django.contrib import admin
from .models import Adress, Order, Customer, Menu_Category, Menu, Extras, Extracategory, Portion
from restaurants.models import Restaurant, Restaurant_Category
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('email',)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Customer
        fields = ('email',)

class CustomerAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('email', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)



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
admin.site.register(Adress)
admin.site.register(Restaurant)
admin.site.register(Restaurant_Category)
admin.site.register(Extras)
admin.site.register(Extracategory)
admin.site.register(Portion)
admin.site.register(Menu_Category)
admin.site.register(Menu)





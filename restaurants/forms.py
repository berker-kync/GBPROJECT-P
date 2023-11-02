from django import forms
from .models import RestaurantRegistration
from fooddelivery.models import Menu




class RestaurantRegistrationForm(forms.ModelForm):

    class Meta:
        model = RestaurantRegistration
        fields = ['email', 'name', 'restaurant_name', 'address', 'province', 'postal_code']

    email = forms.EmailField(label="Email adresi", min_length=2, max_length=50)
    name = forms.CharField(label="Ad Soyad", min_length=2, max_length=50)
    restaurant_name = forms.CharField(label="Restoran İsmi", min_length=5, max_length=60)
    address = forms.CharField(label="Adres", max_length=50)
    province = forms.CharField(label="İlçe", max_length=15)
    postal_code = forms.CharField(label='Posta Kodu', min_length=5, max_length=5)


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant', 'name', 'price', 'description', 'category', 'quantity', 'product_image', 'is_active']



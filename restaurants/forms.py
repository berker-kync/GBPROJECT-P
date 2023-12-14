from django import forms
from .models import Province, RestaurantRegistration
from fooddelivery.models import Menu, Restaurant


class StaffLoginForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))

class RestaurantRegistrationForm(forms.ModelForm):

    class Meta:
        model = RestaurantRegistration
        fields = ['email', 'name', 'restaurant_name', 'address', 'province', 'postal_code']

    email = forms.EmailField(label="Email adresi", min_length=2, max_length=50)
    name = forms.CharField(label="Ad Soyad", min_length=2, max_length=50)
    restaurant_name = forms.CharField(label="Restoran İsmi", min_length=5, max_length=60)
    address = forms.CharField(label="Adres", max_length=50)
    province = forms.ModelChoiceField(label="İlçe", queryset=Province.objects.all())
    postal_code = forms.CharField(label='Posta Kodu', min_length=5, max_length=5)



class MenuItemForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ['restaurant'] 

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)




from django import forms
from .models import Adress, Customer
from .validators import phone_number_validator
from django.contrib.auth.forms import UserCreationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = ['name', 'phone', 'street', 'apartment', 'door_number', 'city', 'postal_code']

    name = forms.CharField(label="Adres İsmi", min_length=2, max_length=50)
    phone = forms.CharField(label="Telefon", max_length=10, validators=[phone_number_validator])
    street = forms.CharField(label="Sokak", min_length=5, max_length=60)
    apartment = forms.CharField(label="Apartman ve Apt. No", max_length=20)
    door_number = forms.CharField(label="İç Kapı No", max_length=3)
    city = forms.CharField(label="Şehir", max_length=20)
    postal_code = forms.CharField(label='Posta Kodu', min_length=5, max_length=5)


class RegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

    
    name = forms.CharField(label="Ad Soyad", min_length=3, max_length=50)
    email = forms.EmailField(label="Email", max_length=100)
    phone = forms.CharField(label="Telefon" ,max_length=10, validators=[phone_number_validator])
    
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'phone': forms.TextInput(attrs={'class': 'form-control'}),
    }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     address = cleaned_data.get('address')
    
    # if not address:
    #     raise forms.ValidationError("Please provide your address.")


class LoginForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))
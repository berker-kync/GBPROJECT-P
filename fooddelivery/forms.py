from cProfile import label
from collections.abc import Mapping
from os import name
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from .models import Customer
from .validators import phone_number_validator
from django.contrib.auth.forms import UserCreationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'postal_code']

    phone = forms.CharField(max_length=20, validators=[phone_number_validator])
    postal_code = forms.CharField(max_length=5, min_length=5)
    name = forms.CharField(min_length=3, max_length=50)
    address = forms.CharField(min_length=15, max_length=150)

class RegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'postal_code']

    
    name = forms.CharField(label="Ad Soyad", min_length=3, max_length=50)
    email = forms.EmailField(label="Email", max_length=100)
    phone = forms.CharField(label="Telefon" ,max_length=10, validators=[phone_number_validator])
    address = forms.CharField(label="Adres" ,min_length=15, max_length=150)
    city = forms.CharField(label="Şehir", max_length=20)
    postal_code = forms.CharField(label="Posta Kodu", max_length=5, min_length=5)
    
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'phone': forms.TextInput(attrs={'class': 'form-control'}),
        'address': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
    }


class LoginForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))

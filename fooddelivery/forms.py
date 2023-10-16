from django import forms
from .models import Customer
from django.core.exceptions import ValidationError
from .validators import *




class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'postal_code']

    phone = forms.CharField(max_length=20, validators=[phone_number_validator])
    name = forms.CharField(validators=[name_validator])
    city = forms.CharField(validators=[city_validator])
    postal_code = forms.CharField(validators=[postcode_validator])


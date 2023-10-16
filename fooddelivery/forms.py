from django import forms
from .models import Customer
from .validators import phone_number_validator

class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'postal_code']

    phone = forms.CharField(max_length=20, validators=[phone_number_validator])






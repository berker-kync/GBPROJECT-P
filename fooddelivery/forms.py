from django import forms
from .models import Customer

class OrderForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'postal_code']




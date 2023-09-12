# forms.py

from django import forms
from .models import CustomUser

class RegularUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    user_type = forms.CharField(widget=forms.HiddenInput(), initial='regular')

class RestaurantManagerRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    user_type = forms.CharField(widget=forms.HiddenInput(), initial='restaurant')

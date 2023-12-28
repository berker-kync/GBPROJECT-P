from django import forms
from .models import Adress, Customer, Province, Review
from .validators import phone_number_validator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('email', 'name', 'phone', 'address', 'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('email', 'name', 'phone', 'address', 'is_active', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = ['name', 'phone', 'street', 'apartment', 'door_number', 'city', 'province', 'postal_code']

    name = forms.CharField(label="Adres İsmi", min_length=2, max_length=50)
    phone = forms.CharField(label="Telefon", max_length=10, validators=[phone_number_validator])
    street = forms.CharField(label="Sokak", min_length=5, max_length=60)
    apartment = forms.CharField(label="Apartman ve Apt. No", max_length=20)
    door_number = forms.CharField(label="İç Kapı No", max_length=3)
    province = forms.ModelChoiceField(label="İlçe", queryset=Province.objects.all())
    city = forms.ChoiceField(label="Şehir", choices=Adress.CITY_CHOICES)
    postal_code = forms.CharField(label='Posta Kodu', min_length=5, max_length=5)


class RegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']

    
    name = forms.CharField(label="Ad Soyad", min_length=3, max_length=50)
    email = forms.EmailField(label="Email", max_length=100)
    
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }


class LoginForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))

class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

    name = forms.CharField(label="Ad Soyad", min_length=3, max_length=50)
    email = forms.EmailField(label="Email", max_length=100, disabled=True)
    phone = forms.CharField(label="Telefon" ,max_length=10, validators=[phone_number_validator])
    
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'phone': forms.TextInput(attrs={'class': 'form-control'}),
    }

class ChangePasswordForm(PasswordChangeForm):
    model = Customer
    fields = ['password1', 'password2']


# REVIEW İÇİN
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'score']
        widgets = {
            'score': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1.0}),
            'title': forms.TextInput(attrs={'placeholder': 'Deneyiminizi bir cümle ile özetleyiniz.'}),
            'content': forms.Textarea(attrs={'placeholder': 'Restoranı ve siparişinizi ifade ediniz.', 'rows': 10}),  
        }
        labels = {
            'score': 'Score (0-10)',
            'title': 'Başlık',
            'content': 'Yorum',
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Adınız', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-posta Adresiniz', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-12', 'rows': 6}), label='Mesajınız')  # rows değerini artırın

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': 10})  # Burada da rows değerini artırın
from django import forms
from .models import Province, RestaurantRegistration
from fooddelivery.models import Menu, Menu_Category
from fooddelivery.validators import phone_number_validator


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit


class StaffLoginForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}))

class RestaurantRegistrationForm(forms.ModelForm):

    class Meta:
        model = RestaurantRegistration
        fields = ['email', 'name', 'phone', 'restaurant_name', 'address', 'province', 'postal_code']

    email = forms.EmailField(label="Email adresi", min_length=2, max_length=50)
    name = forms.CharField(label="Ad Soyad", min_length=2, max_length=50)
    phone = forms.CharField(label="Telefon" ,max_length=10, validators=[phone_number_validator])
    restaurant_name = forms.CharField(label="Restoran İsmi", min_length=5, max_length=60)
    address = forms.CharField(label="Adres", max_length=50)
    province = forms.ModelChoiceField(label="İlçe", queryset=Province.objects.all())
    postal_code = forms.CharField(label='Posta Kodu', min_length=5, max_length=5)





class MenuItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Menu_Category.objects.all(),
        label='Kategori'
    )

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'category', 'quantity', 'product_image']
        labels = {
            'name': 'Ürün İsmi',
            'price': 'Ücret',
            'description': 'Ürün Açıklaması',
            'category': 'Kategori',
            'quantity': 'Ürün Adedi',
            'product_image': 'Ürün Görseli',
        }

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name'),
            Field('price', type='number'),
            Field('description', rows=3),
            Div(
                Field('product_image'),  # Remove custom class here
                HTML('<label for="id_product_image" class="form-label"></label>'),  # Use Bootstrap 5 classes
                css_class='mb-4'  # Add spacing for visual clarity
            ),
            Field('quantity', type='number'),
            # Field('product_image', css_class='custom-file-input'),
            Submit('save', 'Menüye Ekle', css_class='btn btn-primary mt-3')
        )



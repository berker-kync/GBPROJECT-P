from django import forms
from .models import Province, RestaurantRegistration
from fooddelivery.models import Menu, Menu_Category, Portion, Extras
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
        label='Kategori',
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )

    product_image = forms.ImageField(
        label='Ürün Görseli',
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
    )

    # Yeni eklenen alanlar
    portions = forms.ModelMultipleChoiceField(
        queryset=Portion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Porsiyon Seçenekleri'
    )
    extras = forms.ModelMultipleChoiceField(
        queryset=Extras.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Ekstra Seçenekler',
        required=False
    )

    class Meta:
        model = Menu
        fields = ['name', 'price', 'description', 'category', 'quantity', 'product_image', 'portions', 'extras']
        labels = {
            'name': 'Ürün İsmi',
            'price': 'Ücret',
            'description': 'Ürün Açıklaması',
            'category': 'Kategori',
            'quantity': 'Ürün Adedi',
            'product_image': 'Ürün Görseli',
            'portions': 'Porsiyon Seçenekleri',
            'extras': 'Ekstra Seçenekler',
        }

    def __init__(self, *args, **kwargs):

        instance = kwargs.get('instance', None)
        
        # Eğer form bir instance üzerinden başlatılmışsa, 
        # initial değerleri ayarla.
        if instance:
            initial = kwargs.get('initial', {})
            initial['portions'] = instance.portions.values_list('id', flat=True)
            initial['extras'] = instance.extras.values_list('id', flat=True)
            kwargs['initial'] = initial

        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name', css_class='form-control mb-3'),
            Field('price', css_class='form-control mb-3', type='number', min='0'),
            Field('description', css_class='form-control mb-3', rows=3),
            Field('category', css_class='form-control custom-select mb-3'),
            Field('portions', wrapper_class='my-custom-class-for-portions'),
            Field('extras', wrapper_class='my-custom-class-for-extras'),
            Div(
                HTML('<label class="custom-file-label" for="id_product_image">Choose file</label>'),
                Field('product_image', css_class='custom-file-input'),
                css_class='custom-file mb-3'
            ),
            Field('quantity', css_class='form-control mb-3', type='number', min='0'),
            Submit('save', 'Menüye Ekle', css_class='btn btn-primary')
        )

        self.fields['product_image'].widget.attrs.update({'class': 'custom-file-input', 'id': 'id_product_image'})
        self.fields['product_image'].label = 'Ürün Görseli'



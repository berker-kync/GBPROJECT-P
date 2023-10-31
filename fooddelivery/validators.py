from django.core.exceptions import ValidationError
import re

def phone_number_validator(value):
    phone_regex = re.compile(r'^\d{10}$')
    if not phone_regex.match(value):
        raise ValidationError('Geçersiz telefon numarası. Lütfen 10 haneli telefon numarası giriniz.')
    return value

def name_validator(value):
    if len(value) < 3:
        raise ValidationError('En az 3 karakterden oluşmalı.')

    if not re.match("^[a-zA-Z\s]*$", value):
        raise ValidationError('Rakam ya da özel karakter kullanılamaz.')
    
def postcode_validator(value):    
    if len(value) != 5:
        raise ValidationError('Posta kodları 5 haneden oluşur.')
    
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Posta kodu yalnızca rakamlardan oluşur.')
    
def city_validator(value):      
    if not re.match("^[a-zA-Z\s]*$", value):
        raise ValidationError('Rakam ya da özel karakter kullanılamaz.')
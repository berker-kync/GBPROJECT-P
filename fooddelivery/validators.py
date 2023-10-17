from django.core.exceptions import ValidationError
import re

def phone_number_validator(value):
    phone_regex = re.compile(r'^\d{10}$')
    if not phone_regex.match(value):
        raise ValidationError('Geçersiz telefon numarası. Lütfen 10 haneli telefon numarası giriniz.')
    return value
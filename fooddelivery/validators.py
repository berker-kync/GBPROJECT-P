from django.core.exceptions import ValidationError
import re

def phone_number_validator(value):
    phone_regex = re.compile(r'^\d{10}$')
    if not phone_regex.match(value):
        raise ValidationError('Invalid phone number.')
    return value
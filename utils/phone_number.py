from django.core.exceptions import ValidationError
import re

def validate_phone_number(value: str):
    if not value.startswith('+255'):
        raise ValidationError('Phone number must start with +255.')
    
    if not re.match(r'^\+255\d{9,10}$', value):
        raise ValidationError('Phone number must be in the format: +255xxxxxxxxx (9 or 10 digits after +255).')

    if len(value) != 13:
        raise ValidationError('Phone number must be exactly 13 characters long, including +255.')

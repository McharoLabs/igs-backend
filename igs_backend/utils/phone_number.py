from django.core.exceptions import ValidationError
import re

def validate_phone_number(value: str):
    """
    Validates a Tanzanian phone number.
    - Must start with '0'
    - Must be exactly 10 digits long
    - Must contain only digits
    """
    if not value.startswith('0'):
        raise ValidationError('Phone number must start with 0.')

    if not re.match(r'^0\d{9}$', value):
        raise ValidationError('Phone number must be in the format: 0XXXXXXXXX (10 digits).')

    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 characters long.')

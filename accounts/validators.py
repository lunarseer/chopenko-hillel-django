from django.core.exceptions import ValidationError
import re


def change_password_validator(value):
    if not value:
        return None
    if len(value) != 12:
        raise ValidationError('Invalid phone number length, must be 12 digits',
                              params={'value': value})
    elif not re.search(r'\d{12}', value):
        raise ValidationError('Phone number must contains only digits',
                              params={'value': value})
    return None

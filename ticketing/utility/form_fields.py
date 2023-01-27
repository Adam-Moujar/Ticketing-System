from ticketing.const import user_validation

from ticketing.models import User

from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

import copy

user_email = User._meta.get_field("email").formfield()

email = copy.copy(user_email)
email.unique = False

password = forms.CharField(
    label = "Password:",
    widget = forms.PasswordInput(),
    min_length = user_validation.PASSWORD_MIN_LENGTH,
    validators = [
        RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = ("Your password must contain an uppercase character, a lowercase "
                        "character and a number")
            )]
)

confirm_password = copy.copy(password)
confirm_password.label = "Confirm Password"
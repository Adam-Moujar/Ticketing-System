from ticketing.models import User
from ticketing.utility import custom_widgets
from ticketing.forms import SignupForm

from django.core.validators import RegexValidator
from django import forms

import copy

id = forms.IntegerField(label="ID")

first_name = User._meta.get_field("first_name").formfield()
first_name.label = "First Name"

last_name = User._meta.get_field("last_name").formfield()
last_name.label = "Last Name"

email_unique = User._meta.get_field("email").formfield()

email = copy.copy(email_unique)
email.unique = False

# password = SignupForm().fields["password1"]
# confirm_password = SignupForm().fields["password2"]

password = forms.CharField(
    label = "Password:",
    widget = forms.PasswordInput(),
    min_length = 8,
    validators = [
        RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message = ("Your password must contain an uppercase character, a lowercase "
                        "character and a number")
            )]
)

confirm_password = copy.copy(password)
confirm_password.label = "Confirm Password"

account_role = forms.ChoiceField(choices = [(User.Role.STUDENT, "Student"),
                                            (User.Role.SPECIALIST, "Specialist"),
                                            (User.Role.DIRECTOR, "Director")],
                                            
                                 widget = custom_widgets.ClearableRadioSelect(),
                                 label = "Account Role:",
                                 required = True)
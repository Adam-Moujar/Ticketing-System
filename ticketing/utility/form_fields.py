from ticketing.models import User
from ticketing.utility import custom_widgets
from ticketing.forms import SignupForm

from django.core.validators import RegexValidator
from django import forms

import copy

# Some form fields are stored here that can be reused directly or copied and edited

id = forms.IntegerField(label="ID")

first_name = User._meta.get_field("first_name").formfield()
first_name.label = "First Name"

last_name = User._meta.get_field("last_name").formfield()
last_name.label = "Last Name"

email_unique = User._meta.get_field("email").formfield()

email = copy.copy(email_unique)
email.unique = False

password = SignupForm().fields["password1"]

confirm_password = SignupForm().fields["password2"]

account_role = forms.ChoiceField(choices = [(User.Role.STUDENT, "Student"),
                                            (User.Role.SPECIALIST, "Specialist"),
                                            (User.Role.DIRECTOR, "Directors")],
                                            
                                 widget = custom_widgets.ClearableRadioSelect(),
                                 label = "Account Role:",
                                 required = True)
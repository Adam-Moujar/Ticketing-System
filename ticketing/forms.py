from ticketing.utility import form_fields
from ticketing.models import User

from django import forms

class LoginForm(forms.ModelForm):

    password = form_fields.password

    class Meta:
        model = User
        fields = ['email', 'password']

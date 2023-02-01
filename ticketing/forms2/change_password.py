from ticketing.utility import form_fields
from ticketing.utility.user import user_exists_by_email
from ticketing.models import User

from django import forms

import copy

class ChangePasswordForm(forms.Form):

    password = form_fields.password
    confirm_password = form_fields.confirm_password

    def clean(self):
        super().clean()

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:

            self.add_error('confirm_password', "Passwords don't match")
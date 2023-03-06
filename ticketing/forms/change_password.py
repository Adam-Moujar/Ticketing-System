from ticketing.utility import form_fields
from ticketing.utility.user import user_exists_by_email
from ticketing.models import User

from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

import copy


class ChangePasswordForm(forms.Form):

    password = form_fields.password
    confirm_password = form_fields.confirm_password

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")

        if confirm_password:
            try:
                password_validation.validate_password(
                    confirm_password, self.user
                )
            except ValidationError as error:
                self.add_error('confirm_password', error)

    # def _post_clean(self):
    #     super()._post_clean

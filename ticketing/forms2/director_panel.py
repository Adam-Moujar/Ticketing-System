from ticketing.utility import form_fields
from ticketing.models import User

from django import forms

import copy

class DirectorFilterForm(forms.Form):
    id = copy.copy(form_fields.id)
    id.required = False

    first_name = copy.copy(form_fields.first_name)
    first_name.required = False

    last_name = copy.copy(form_fields.last_name)
    last_name.required = False

    email = forms.CharField(label = form_fields.email.label, required = False)

    role = copy.copy(form_fields.role)
    role.required = False

class DirectorCommandsForm(forms.Form):

    commands_role = copy.copy(form_fields.role)
    commands_role.required = False


class AddUserForm(forms.ModelForm):

    password = form_fields.password

    add_user_role = form_fields.role

    add_user_department = form_fields.department

    class Meta:

        model = User
        fields = ['email', 'first_name', 'last_name', 'password', "add_user_role", "add_user_department"]

        labels = {
            'first_name': "First Name",
            'last_name': "Last Name"
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower()

        return email

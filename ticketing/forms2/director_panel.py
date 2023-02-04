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

    role = form_fields.make_role_radio_select(False)
    role.required = False

    filter_department = copy.copy(form_fields.department)
    filter_department.required = False
    filter_department.disabled = False

class DirectorCommandsForm(forms.Form):

    commands_role = form_fields.make_role_radio_select(True, "commands_department")
    commands_role.required = False

    commands_department = form_fields.department


class AddUserForm(forms.ModelForm):

    password = form_fields.password

    add_user_role = form_fields.make_role_radio_select(True, "add_user_department")

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

from ticketing.utility import form_fields
from ticketing.models import User
from ticketing.forms2.utility.mixins import UserDepartmentFormMixin, ExtendedUserFormMixin

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


def make_add_user_form_class(generated_form_class):

    class AddUserForm(ExtendedUserFormMixin, UserDepartmentFormMixin, generated_form_class):
        department_field_name = "edit_department"
        role_field_name = "edit_role"

    return AddUserForm
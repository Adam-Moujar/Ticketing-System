from ticketing.utility import form_fields
from ticketing.models import User
from ticketing.utility.department import get_department
from ticketing.forms2.utility.mixins import (
    UserDepartmentFormMixin,
    ExtendedUserFormMixin,
)
from ticketing.models.specialist import SpecialistDepartment

from django import forms

import copy


class DirectorFilterForm(forms.Form):
    id = copy.copy(form_fields.id)
    id.required = False

    first_name = copy.copy(form_fields.first_name)
    first_name.required = False

    last_name = copy.copy(form_fields.last_name)
    last_name.required = False

    email = forms.CharField(label=form_fields.email.label, required=False)

    filter_role = form_fields.make_role_radio_select(False)
    filter_role.required = False

    filter_department = copy.copy(form_fields.department)
    filter_department.required = False
    filter_department.disabled = False


class DirectorCommandsForm(UserDepartmentFormMixin, forms.Form):
    department_field_name = 'commands_department'
    role_field_name = 'commands_role'

    commands_role = form_fields.make_role_radio_select(
        True, department_field_name
    )
    commands_role.required = False

    commands_department = form_fields.department


def make_add_user_form_class(generated_form_class):
    class AddUserForm(
        ExtendedUserFormMixin, UserDepartmentFormMixin, generated_form_class
    ):
        department_field_name = 'add_department'
        role_field_name = 'add_role'

        def save(self, commit=True):

            result = super().save(commit=commit)

            if self.cleaned_data['add_role'] == User.Role.SPECIALIST:
                SpecialistDepartment(
                    specialist=self.instance,
                    department=self.cleaned_data['add_department'],
                ).save()

            return result

    return AddUserForm

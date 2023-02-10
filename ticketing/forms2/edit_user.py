from ticketing.utility import form_fields
from ticketing.utility.user import user_exists_by_email
from ticketing.models import User
from ticketing.forms2.utility.mixins import UserDepartmentFormMixin, ExtendedUserFormMixin

from django import forms

import copy

def make_edit_user_form_class(generated_form_class):

    class EditUserForm(ExtendedUserFormMixin, UserDepartmentFormMixin, generated_form_class):
        department_field_name = "edit_department"
        role_field_name = "edit_role"

    return EditUserForm

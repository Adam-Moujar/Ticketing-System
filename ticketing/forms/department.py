from ticketing.utility import form_fields

from django import forms

import copy


class DepartmentFilterForm(forms.Form):
    id = copy.copy(form_fields.id)
    id.required = False

    name = copy.copy(form_fields.department_name)
    name.required = False

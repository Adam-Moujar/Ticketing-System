from ticketing.utility import form_fields
from ticketing.models import User

from django import forms

import copy

class AbstractUserDepartmentForm():

    def __init__(self, data = None, *args, **kwargs):

        super().__init__(data = data, *args, **kwargs)

        if data != None:
            if data.get(self.role_field_name) == User.Role.SPECIALIST:
                self.fields[self.department_field_name].disabled = False

    def clean(self):

        super().clean()

        if self.cleaned_data.get(self.role_field_name) == User.Role.SPECIALIST:
            if self.cleaned_data.get(self.department_field_name) == None:
                self.add_error(self.department_field_name, "You have not selected a user department")
         
        

from ticketing.utility import form_fields
from ticketing.utility.user import user_exists_by_email
from ticketing.models import User


from django import forms

import copy

class EditUserForm(forms.ModelForm):

    # It is required that a valid user is passed to this form.
    # Therefore all views that use this form must validate the user themselves.
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditUserForm, self).__init__(*args, **kwargs)

    update_email = form_fields.email
    edit_role = form_fields.role

    class Meta:
        model = User
        fields = ['update_email', 'first_name', 'last_name', 'edit_role']

    def clean_update_email(self):
        update_email = self.cleaned_data['update_email']
        update_email = update_email.lower()

        return update_email

    def clean(self):
        super().clean()

        email = self.cleaned_data.get('update_email')
        edit_role = self.cleaned_data.get('edit_role')

        if email != self.user.email and user_exists_by_email(email):
            self.add_error('update_email',
                            "Email is being used by another account")

        elif not edit_role:
            self.add_error('edit_role',
                            "Please select an account type")

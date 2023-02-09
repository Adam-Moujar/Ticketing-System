from ticketing.forms2.edit_user import make_edit_user_form_class
from ticketing.models import User, Department
from ticketing import utility
from ticketing.utility import get
from ticketing.utility.get import get_user_from_id_param
from ticketing.utility import form_fields

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import UpdateView

class EditUserView(UpdateView):

    model = User
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy("director_panel")


    def get_template_names(self):
        return ["edit_user.html"]


    def get_form(self, form_class = None):

        form_class = self.get_form_class()

        _class = make_edit_user_form_class(form_class)
        
        form = _class(**self.get_form_kwargs())

        return form


    def post(self, request, *args, **kwargs):

        if request.POST.get("cancel"):
            return get.redirect_to_director_panel_with_saved_params(request)

        return super().post(request, *args, **kwargs)


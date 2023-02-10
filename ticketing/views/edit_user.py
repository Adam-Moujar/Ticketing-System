from ticketing.forms2.edit_user import make_edit_user_form_class
from ticketing.models import User, Department
from ticketing import utility
from ticketing.utility import get
from ticketing.utility.get import get_user_from_id_param
from ticketing.utility import form_fields
from ticketing.views.utility.mixins import DynamicCustomFormClassMixin

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import UpdateView

class EditUserView(DynamicCustomFormClassMixin, UpdateView):

    model = User

    # We will dynamically add the other fields (role, department) later, so they are missing from this list
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy("director_panel")

    form_class_maker = make_edit_user_form_class


    def get_template_names(self):
        return ["edit_user.html"]


    def post(self, request, *args, **kwargs):

        if request.POST.get("cancel"):
            return get.redirect_to_director_panel_with_saved_params(request)

        return super().post(request, *args, **kwargs)


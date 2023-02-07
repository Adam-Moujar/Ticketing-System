from ticketing.forms2.director_panel import DirectorFilterForm, DirectorCommandsForm, AddUserForm
from ticketing.models import User, Department

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from ticketing.forms import *
from django.views.generic.edit import UpdateView

class EditDepartmentView(UpdateView):
    model = Department
    fields = ['name']
    success_url = reverse_lazy("department_manager")


    def get_template_names(self):
        return ["edit_department.html"]

    def post(self, request, *args, **kwargs):

        if(request.POST.get("cancel")):
            return redirect("department_manager")
        
        return super().post(request, *args, **kwargs)





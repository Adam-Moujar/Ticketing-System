from ticketing.forms2.director_panel import DirectorFilterForm, DirectorCommandsForm, AddUserForm
from ticketing.models import User

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password


class DepartmentManagerView(ListView):

    def get(self, request):
        return render(request, "department_manager.html", {})



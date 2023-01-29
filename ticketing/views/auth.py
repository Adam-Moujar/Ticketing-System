from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.messages.views import SuccessMessageMixin
from ticketing.forms import SignupForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = "Your account was created successfully"
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from ticketing.forms import SignupForm, LoginForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = "Your account was created successfully"

class CustomLoginView(LoginView):
    def get_success_url(self):
        match self.request.user.role:
            case 'ST':
                return reverse('home')
            case 'SP':
                return reverse('specialist_dashboard')
            case default:
                return reverse('home')


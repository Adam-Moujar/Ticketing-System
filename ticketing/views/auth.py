from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from ticketing.forms import SignupForm, LoginForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = "Your account was created successfully"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super().get(request, *args, **kwargs)

class CustomLoginView(LoginView):
    def get_success_url(self):
        match self.request.user.role:
            case 'ST':
                return reverse('home')
            case 'SP':
                return reverse('specialist_dashboard')
            case default:
                return reverse('home')


from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from django.urls import reverse

from django.contrib.messages.views import SuccessMessageMixin
from ticketing.forms import SignupForm, LoginForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from ticketing.const import role as Role

class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = "Your account was created successfully"

class CustomLoginView(LoginView):
    def get_success_url(self):
        match self.request.user.role:
            case Role.STUDENT:
                return reverse('home')
            case Role.SPECIALIST:
                return reverse('specialist_dashboard')
            case default:
                return reverse('home')

# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.role == Role.STUDENT:
#                 return redirect(reverse('home'))
#             if user.role == Role.SPECIALIST:
#                 return redirect(reverse('specialist_dashboard'))

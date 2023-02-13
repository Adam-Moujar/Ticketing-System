from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from ticketing.forms import SignupForm, LoginForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = SignupForm
    success_message = "Your account was created successfully"

    #redirects authenticated users
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    def get_success_url(self):
        match self.request.user.role:
            case 'ST':
                return reverse('student_dashboard')
            case 'SP':
                return reverse('specialist_dashboard')
            case 'DI':
                return reverse('home')


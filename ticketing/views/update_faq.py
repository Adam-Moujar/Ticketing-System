from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ticketing.forms.specialist_faq import FAQForm
from django.urls import reverse, reverse_lazy
from ticketing.models.faq import FAQ
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.views.generic.edit import UpdateView


class FAQUpdateFormView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    template_name = 'faq_update.html'
    required_roles = ['SP', 'DI']
    form_class = FAQForm
    success_url = reverse_lazy('home')
    model = FAQ

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

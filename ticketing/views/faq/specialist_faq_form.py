from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ticketing.forms.specialist_faq import FAQForm
from django.urls import reverse, reverse_lazy
from ticketing.models.faq import FAQ
from ticketing.models.users import User
from ticketing.models.departments import Department
from ticketing.models.specialist import SpecialistDepartment
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin


class FAQFormView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'faq_specialist_form.html'
    required_roles = ['SP', 'DI']
    form_class = FAQForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        form.custom_save(
            specialist=self.request.user,
            department=SpecialistDepartment.objects.get(
                specialist=self.request.user
            ).department,
            questions=form.cleaned_data['questions'],
            subsection=form.cleaned_data['subsection'],
            answer=form.cleaned_data['answer'],
        )
        return HttpResponseRedirect(self.get_success_url())

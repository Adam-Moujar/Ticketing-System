from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ticketing.forms.specialist_faq import FAQForm
from django.urls import reverse, reverse_lazy
from ticketing.models.specialist import SpecialistDepartment
from ticketing.models.departments import Subsection
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.contrib import messages


class FAQFormView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'faq_specialist_form.html'
    required_roles = ['SP', 'DI']
    form_class = FAQForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        specialist_department = SpecialistDepartment.objects.get(
            specialist=self.request.user
        )
        kwargs['department'] = specialist_department.department
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        print('Dispatch method called')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print('hi')
        form.custom_save(
            specialist=self.request.user,
            department=SpecialistDepartment.objects.get(
                specialist=self.request.user
            ).department,
            questions=form.cleaned_data['questions'],
            subsection=form.cleaned_data['subsection'],
            answer=form.cleaned_data['answer'],
        )
        messages.info(self.request, 'FAQ has been created')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form, **kwargs):
        print('hi invalid')
        return self.render_to_response(self.get_context_data())

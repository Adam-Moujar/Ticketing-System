from django.views.generic import FormView
from ticketing.models.departments import Subsection
from ticketing.models.specialist import SpecialistDepartment
from ticketing.forms.subsection import SubsectionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.urls import reverse, reverse_lazy

class SpecialistSubSectionView(LoginRequiredMixin, RoleRequiredMixin, FormView): 
    model = Subsection
    required_roles = ['SP']
    template_name = "create_subsection.html"
    form_class = SubsectionForm
    success_url = reverse_lazy('home')

    def formvalid(self, form):
        form.custom_save(
            department=SpecialistDepartment.objects.get(
                specialist=self.request.user
            ).department,
            subsection=form.cleaned_data['subsection'],
        )
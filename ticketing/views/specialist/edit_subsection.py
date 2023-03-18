from ticketing.models.departments import Subsection
from ticketing.models.specialist import SpecialistDepartment
from ticketing.models.users import User
from ticketing.forms.subsection import SubsectionForm
from ticketing.mixins import RoleRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class EditSubsectionView(LoginRequiredMixin, RoleRequiredMixin, UpdateView): 
    model = Subsection
    required_roles = [User.Role.SPECIALIST]
    template_name = "specialist/edit_subsection.html"
    form_class = SubsectionForm
    success_url = reverse_lazy('subsection_manager')
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            return redirect('subsection_manager')
        return super().post(request, *args, **kwargs)
    

from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from ticketing.models.faq import FAQ
from ticketing.models.departments import Department
from ticketing.models.specialist import SpecialistDepartment
from ticketing.models.users import User
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin


class SpecialistDepartmentFaq(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = FAQ
    template_name = 'specialist_department_faq.html'
    required_roles = ['SP', 'DI']
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user
        department = SpecialistDepartment.objects.get(
            specialist=user
        ).department
        return FAQ.objects.filter(department=department)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        specialist_dept = SpecialistDepartment.objects.get(
            specialist=user
        ).department
        department = get_object_or_404(Department, name=specialist_dept)
        context['department_name'] = department.name
        return context

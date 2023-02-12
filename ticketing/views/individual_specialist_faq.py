from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from ticketing.models.faq import FAQ
from ticketing.models.departments import Department
from ticketing.models.users import User
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin


class SpecialistFAQListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = FAQ
    template_name = 'individual_faq_list.html'
    required_roles = ['SP', 'DI']
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        return FAQ.objects.filter(specialist=user)

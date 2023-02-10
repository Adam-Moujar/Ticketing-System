from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from ticketing.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin


class StudentInboxView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Ticket
    required_roles = ['ST']
    template_name = 'student_inbox.html'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        return Ticket.objects.filter(student_id=self.request.user.id)

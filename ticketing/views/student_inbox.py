from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from ticketing.models import Ticket


class StudentInboxView(ListView):
    model = Ticket
    template_name = 'student_inbox.html'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        return Ticket.objects.filter(student_id=self.request.user.id)

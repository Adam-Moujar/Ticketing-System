from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from ticketing.models import * 

class StudentInboxView(ListView):  
    model = Ticket
    template_name = 'student_inbox.html'
    paginate_by = 5  # if pagination is desired
    def get_queryset(self):
        return Ticket.objects.filter(student_id = self.request.user.id, status = 'open')

class ClosedInboxView(ListView):
    model = Ticket
    template_name = 'closed_inbox.html'
    paginate_by = 5
    def get_queryset(self):
        return Ticket.objects.filter(student_id = self.request.user.id, status = 'closed')

# class StatusInboxView(ListView):
#     model = Ticket
#     template_name = 'status_inbox.html'
#     paginate_by = 5
#     slug_field = 'status'

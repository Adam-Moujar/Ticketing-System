from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed

from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment

@method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class TicketView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ticket.html')
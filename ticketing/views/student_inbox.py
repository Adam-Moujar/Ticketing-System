from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from ticketing.models import *
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed

import copy


@method_decorator(roles_allowed(allowed_roles=['ST']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class StudentInboxView(ListView):
    model = Ticket
    template_name = 'student_dashboard.html'
    paginate_by = 5  # if pagination is desired

    def get_queryset(self):
        tickets = Ticket.objects.filter(student_id=self.request.user.id)
        if self.request.method == 'GET':   # Gets all tickets from that user
            return tickets

        if self.request.method == 'POST':
            ticket_type = self.request.POST.get('type_of_ticket')
            match ticket_type:
                case 'Open':
                    return tickets.filter(status='Open')
                case 'Closed':
                    return tickets.filter(status='Closed')
                case default:
                    return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_type = ''
        if self.request.method == 'POST':
            ticket_type = self.request.POST.get('type_of_ticket')

        context['type_of_ticket'] = ticket_type
        return context

    def post(self, request, *args, **kwargs):

        # request.GET["page"] = 1

        get_copy = copy.copy(request.GET)
        get_copy['page'] = 1

        request.GET = get_copy

        context = {
            'page_obj': self.get_queryset(),
            'type_of_ticket': self.request.POST.get('type_of_ticket'),
        }

        context.update(super().get(request).context_data)

        return render(request, 'student_dashboard.html', context)

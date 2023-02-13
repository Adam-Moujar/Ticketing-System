from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin

from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment


class SpecialistInboxView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Ticket
    template_name = 'specialist_dashboard.html'
    required_roles = ['SP', 'DI']

    def get_queryset(self):
        user = self.request.user
        user_department = SpecialistDepartment.objects.filter(specialist=user)

        ticket_list = []
        if self.request.method == 'POST':
            ticket_type = self.request.POST.get('type_of_ticket')
            ticket_list = self.get_tickets(user, user_department, ticket_type)

        if self.request.method == 'GET':
            ticket_type = 'personal'
            ticket_list = self.get_tickets(user, user_department, ticket_type)

        return ticket_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_type = ''

        if self.request.method == 'POST':
            ticket_type = self.request.POST.get('type_of_ticket')

        if self.request.method == 'GET':
            ticket_type = 'personal'

        context['ticket_type'] = ticket_type
        return context

    def post(self, request, *args, **kwargs):
        return render(
            request,
            'specialist_dashboard.html',
            {
                'object_list': self.get_queryset(),
                'ticket_type': self.request.POST.get('type_of_ticket'),
            },
        )

    def get_tickets(self, user, user_department, ticket_type):
        match ticket_type:
            case 'department':
                if len(user_department) != 0:
                    full_ticket_list = Ticket.objects.filter(
                        department=user_department.first().department
                    )
                    ticket_list = []
                    for ticket in full_ticket_list:
                        if (
                            len(SpecialistInbox.objects.filter(ticket=ticket))
                            == 0
                        ):
                            ticket_list.append(ticket)

            case 'personal':
                ticket_list = Ticket.objects.filter(
                    id__in=SpecialistInbox.objects.filter(
                        specialist=user
                    ).values_list('ticket_id', flat=True)
                )

            case default:
                ticket_list = []

        return ticket_list

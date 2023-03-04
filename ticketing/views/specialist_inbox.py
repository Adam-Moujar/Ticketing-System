from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin

from ticketing.models import (
    User,
    Ticket,
    SpecialistInbox,
    SpecialistDepartment,
)
from ticketing.views.utility.mixins import FilterView

from ticketing.forms.specialist_inbox import SpecialistInboxFilterForm


class SpecialistInboxView(
    LoginRequiredMixin, RoleRequiredMixin, FilterView, ListView
):
    model = Ticket
    template_name = 'specialist_dashboard.html'
    required_roles = ['SP']

    paginate_by = 10

    filter_form_class = SpecialistInboxFilterForm
    filter_preserved_get_params = [['type_of_ticket', 'personal']]

    def setup(self, request, ticket_type, *args, **kwargs):
        self.ticket_type = ticket_type

        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        ticket_list = []

        if self.request.method == 'POST':
            if 'unclaim' in self.request.POST:
                self.unclaim_ticket(self.request.POST['unclaim'])
                self.ticket_type = 'personal'

        students_by_email = User.objects.filter(
            role=User.Role.STUDENT,
            email__istartswith=self.filter_data['email'],
        )

        full_ticket_list = Ticket.objects.filter(
            student__in=students_by_email,
            header__istartswith=self.filter_data['header'],
        )

        ticket_list = self.get_tickets(
            user, self.ticket_type, full_ticket_list
        )

        return ticket_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ticket_type = self.request.GET.get('type_of_ticket')

        if ticket_type == None:
            ticket_type = 'personal'

        context['ticket_type'] = self.ticket_type
        context['inbox_type'] = self.set_formatted_inbox_name(self.ticket_type)
        context['department_name'] = self.get_department_name()
        return context

    def get(self, request, *args, **kwargs):
        if self.ticket_type not in ['personal', 'archived', 'department']:
            return redirect('specialist_dashboard', ticket_type='personal')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'unclaim' in self.request.POST:
            self.ticket_type = 'personal'

        if 'reroute' in self.request.POST:
            pass

        result = super().post(request, *args, **kwargs)

        if result != None:
            return result

        return super().get(request, *args, **kwargs)

    def get_tickets(self, user, ticket_type, full_ticket_list):
        user_department = SpecialistDepartment.objects.filter(specialist=user)
        ticket_list = []

        match ticket_type:
            case 'department':
                if len(user_department) != 0:
                    full_ticket_list = full_ticket_list.filter(
                        department=user_department.first().department
                    ).exclude(status='Closed')
                    ticket_list = []
                    for ticket in full_ticket_list:
                        if (
                            len(SpecialistInbox.objects.filter(ticket=ticket))
                            == 0
                        ):
                            ticket_list.append(ticket)

            case 'personal':
                specialist_tickets = SpecialistInbox.objects.filter(
                    specialist=user
                ).values_list('ticket_id', flat=True)
                ticket_list = []
                for ticket_id in specialist_tickets:
                    ticket = full_ticket_list.filter(id=ticket_id)

                    if len(ticket) > 0:
                        ticket_list.append(ticket[0])

            case 'archived':
                if len(user_department) != 0:
                    ticket_list = full_ticket_list.filter(
                        department=user_department.first().department
                    ).filter(status='Closed')

            case default:
                ticket_list = []

        return ticket_list

    def set_formatted_inbox_name(self, ticket_type):
        match ticket_type:
            case 'department':
                user = self.request.user
                user_department = SpecialistDepartment.objects.filter(
                    specialist=user
                )
                return self.get_department_name() + ' Inbox'
            case 'personal':
                return 'Personal Inbox:'
            case 'archived':
                return 'Archived inbox'
            case default:
                return 'Default'

    def get_department_name(self):
        try:
            user = self.request.user
            specialist_department = SpecialistDepartment.objects.filter(
                specialist=user
            )
            return specialist_department.first().department.name
        except:
            return 'Department has not been found'

    def unclaim_ticket(self, ticket_id):
        SpecialistInbox.objects.filter(
            ticket=Ticket.objects.get(id=ticket_id)
        ).delete()

from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin

from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment


class SpecialistInboxView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Ticket
    template_name = 'specialist_dashboard.html'
    required_roles = ['SP']

    def get_queryset(self):
        '''
        Returning the queryset of tickets based on the selected ticket type.
        
        If the request method is POST, it gets the ticket type from the form and filters the tickets 
        based on the type and the user. If the method is GET, it defaults to "personal" ticket type
        and filters the tickets based on the user.
        
        Args:
            self: object
                An instance of the class that defines this method.
                Used to get the currently logged in user.
        Returns:
            ticket_list: QuerySet
                A queryset of tickets filtered based on the user and the ticket type.
        
        '''
        user = self.request.user
        ticket_list = []

        if self.request.method == 'POST':
            ticket_type = self.request.POST.get('type_of_ticket')
            ticket_list = self.get_tickets(user, ticket_type)

        if self.request.method == 'GET':
            ticket_type = 'personal'
            ticket_list = self.get_tickets(user, ticket_type)

        return ticket_list

    def get_context_data(self, **kwargs):
        '''
        Get the context data that will be passed into the template.
        
        Args:
            self: object
                An instance of the class that defines this method.
            **kwargs: dict
                Context dictionary to be passed into template:
                    -context['ticket_type']= ticket_type //e.g. 'personal'
                    -context['inbox_type']= self.set_formatted_inbox_name(ticket_type) //e.g. 'Personal', 'Archive', 'Department' etc.
                    -context['department_name'] = self.get_department_name() //e.g. 'Accomodation'
        Returns:
            context: dict
                Returning the context dictionary to the template.
                
        '''
        context = super().get_context_data(**kwargs)
        ticket_type = ''

        if self.request.method == 'GET':
            ticket_type = 'personal'

        context['ticket_type'] = ticket_type
        context['inbox_type'] = self.set_formatted_inbox_name(ticket_type)
        context['department_name'] = self.get_department_name()
        return context

    def post(self, request):
        ticket_type = self.request.POST.get('type_of_ticket')
        return render(
            request,
            'specialist_dashboard.html',
            {
                'object_list': self.get_queryset(),
                'ticket_type': ticket_type,
                'inbox_type': self.set_formatted_inbox_name(ticket_type),
                'department_name': self.get_department_name(),
            },
        )

    def get_tickets(self, user, ticket_type):
        user_department = SpecialistDepartment.objects.filter(specialist=user)
        ticket_list = []
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
                specialist_tickets = SpecialistInbox.objects.filter(
                    specialist=user
                ).values_list('ticket_id', flat=True)
                ticket_list = []
                for ticket_id in specialist_tickets:
                    ticket = Ticket.objects.get(id=ticket_id)
                    ticket_list.append(ticket)

            case 'archived':
                if len(user_department) != 0:
                    ticket_list = Ticket.objects.filter(
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

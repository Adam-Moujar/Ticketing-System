from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.shortcuts import redirect


from ticketing.models import (
    Ticket,
    SpecialistInbox,
    SpecialistDepartment,
    Message,
)


class SpecialistClaimTicketView(LoginRequiredMixin, RoleRequiredMixin, View):
    template_name = 'specialist_claim_ticket.html'
    required_roles = ['SP']

    def get(self, request, *args, **kwargs):
        user = request.user
        # CHECK IF THE TICKET WE ARE VIEWING CAN BE VIEWED BY SPECIALIST
        ticket = Ticket.objects.filter(id=self.kwargs['pk'])

        return self.validate_view_ticket(
            user, self.get_department(), ticket, request
        )

    def post(self, request, *args, **kwargs):
        ticket_id = self.request.POST.get('accept_ticket')
        ticket_list = Ticket.objects.filter(id=ticket_id)
        if len(ticket_list) == 0:
            return redirect('specialist_dashboard', ticket_type='department')
        else:
            SpecialistInbox.objects.create(
                specialist=request.user, ticket=ticket_list[0]
            )

        return redirect('specialist_dashboard', ticket_type='department')

    def validate_view_ticket(self, user, department, ticket, request):
        if len(ticket) > 0 and department == ticket[0].department:
            message = Message.objects.filter(ticket=ticket.first()).first()
            return render(
                request,
                self.template_name,
                {
                    'ticket': ticket.first(),
                    'message': message,
                    'department_name': self.get_department().name,
                },
            )
        else:

            return redirect('specialist_dashboard', ticket_type='department')

    def get_department(self):
        try:
            user = self.request.user
            department = (
                SpecialistDepartment.objects.filter(specialist=user).first()
            ).department
            return department
        except:
            return 'Department has not been found'

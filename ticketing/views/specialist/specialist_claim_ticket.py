from django.shortcuts import render
from django.views import View
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

    def get(self, request,*args, **kwargs):
        '''
        The get method overridden in the Class-based view to validate whether
        the user can or cannot view the ticket.
        
        Args:
            self: object
                An instance of the class that defines this method.
                Used to get the currently logged in user.
            request: HttpRequest
                The HTTP request object.
        Returns:
            HttpResponse
                Returns a HttpResponse object if the user is allowed,
                and if the ticket exists.
        Raises:
            Http404:
                If the ticket is not found or the user is not allowed 
                to access the ticket.

        '''
        user = request.user
        # CHECK IF THE TICKET WE ARE VIEWING CAN BE VIEWED BY SPECIALIST
        department = (
            SpecialistDepartment.objects.filter(specialist=user).first()
        ).department
        ticket = Ticket.objects.filter(id=self.kwargs['pk'])

        return self.validate_view_ticket(user, department, ticket, request)

    def post(self, request,*args, **kwargs):
        '''
        Handle the POST request to accept a ticket and 
        add it to the specialist's inbox.
        
        Args:
            self: object
                An instance of the class that defines this method.
            request: HttpRequest
                The HTTP request object representing the current user.
        Returns:
            HttpResponseRedirect
                Redirects the response to the specialist dashboard.
                
        '''
        ticket_id = self.request.POST.get('accept_ticket')
        ticket_list = Ticket.objects.filter(id=ticket_id)
        if len(ticket_list) == 0:
            return redirect('/specialist_dashboard')
        else:
            SpecialistInbox.objects.create(
                specialist=request.user, ticket=ticket_list[0]
            )

        return redirect('/specialist_dashboard')

    def validate_view_ticket(self, user, department, ticket, request):
        '''
        Validates if the current user has permission to view the given ticket.
        
        Args:
            department: Department
                The department that the current user belongs to.
            ticket: QuerySet
                A queryset containing the ticket object to be viewed.
            request: HttpRequest
                The HttpRequest object.
            user: User
                The logged in user to be validated.
        Returns:
            Returning a response object with the ticket details only
            if the user has permission, otherwise redirects to the specialist 
            dashboard page.
            
        '''
        if len(ticket) > 0 and department == ticket[0].department:
            message = Message.objects.filter(ticket=ticket.first()).first()
            return render(
                request,
                self.template_name,
                {
                    'ticket': ticket.first(),
                    'message': message,
                    'department_name': self.get_department_name(),
                },
            )
        else:

            return redirect('/specialist_dashboard')

    def get_department_name(self):
        '''
        Getting the name of the department of the specialist.
        
        Args:
            self: object
                An instance of the class that defines this method.
                Used to get the currently logged in user.
        Returns:
            str
                The name of the department that the specialist belongs to.
                If the department does not exists, return 'Department has not
                been found'
        '''
        try:
            user = self.request.user
            specialist_department = SpecialistDepartment.objects.filter(
                specialist=user
            )
            return specialist_department.first().department.name
        except:
            return 'Department has not been found'

from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.shortcuts import redirect
from itertools import chain
from operator import attrgetter

from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ticketing.forms.specialist_faq import FAQForm
from django.urls import reverse, reverse_lazy

from ticketing.models import SpecialistDepartment,SpecialistMessage, FAQ, StudentMessage, Message
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin



from ticketing.models import (
    Ticket,
    SpecialistDepartment,
)

class SpecialistCreateFAQFromTicketView(LoginRequiredMixin, RoleRequiredMixin, FormView, ListView):
    template_name = 'faq/specialist_create_faq_from_ticket.html'
    required_roles = ['SP']
    form_class = FAQForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        specialist_department = SpecialistDepartment.objects.get(
            specialist=self.request.user
        )
        kwargs['department'] = specialist_department.department
        return kwargs

    def form_valid(self, form):
        '''
        Save the form data and redirect to the specialist dashboard.
        
        Args:
            self: object
                An instance of the class that defines the method.
            form : TicketForm
                The validated form object containing the ticket data.
        Returns:
            response : HttpResponse
                A redirect to the specialist dashboard with the ticket type parameter set to 'personal'.
        '''
        form.custom_save(
            specialist=self.request.user,
            department=SpecialistDepartment.objects.get(
                specialist=self.request.user
            ).department,
            question=form.cleaned_data['question'],
            subsection=form.cleaned_data['subsection'],
            answer=form.cleaned_data['answer'],
        )
        return redirect('specialist_dashboard', ticket_type='personal')

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     # CHECK IF THE TICKET WE ARE VIEWING CAN BE VIEWED BY SPECIALIST
    #     ticket = Ticket.objects.filter(id=self.kwargs['pk'])
    #     messsages = Message.objects.filter(
    #         ticket=self.kwargs['pk']
    #     )

    #     return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        '''
        Retrieve and return the message associated with the current ticket.
        
        Args:
            self: object
                An instance of the class that defines the method.
        Returns:
            queryset: [Message]
                The messages associated with the current ticket, sorted by date and time in descending order.
        '''
        student_message = StudentMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        specialist_message = SpecialistMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        queryset = sorted(
            chain(student_message, specialist_message),
            key=attrgetter('date_time'),
            reverse=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id=self.kwargs['pk'])
        return context








    
    # required_roles = ['SP']

    # def get(self, request,*args, **kwargs):
    #     user = request.user
    #     # CHECK IF THE TICKET WE ARE VIEWING CAN BE VIEWED BY SPECIALIST
    #     department = (
    #         SpecialistDepartment.objects.filter(specialist=user).first()
    #     ).department
    #     ticket = Ticket.objects.filter(id=self.kwargs['pk'])
    #     #return render(request, self.template_name)
    #     return self.validate_view_ticket(user, department, ticket, request)
    
    # def validate_view_ticket(self, user, department, ticket, request):
    #     if len(ticket) > 0 and department == ticket[0].department:
    #         message = Message.objects.filter(ticket=ticket.first()).first()
    #         return render(
    #             request,
    #             self.template_name,
    #             {
    #                 'ticket': ticket.first(),
    #                 'message': message,
    #                 'department_name': self.get_department_name(),
    #             },
    #         )
    #     else:

    #         return redirect('specialist_dashboard', ticket_type="department")
        
    # def get_department_name(self):
    #     try:
    #         user = self.request.user
    #         specialist_department = SpecialistDepartment.objects.filter(
    #             specialist=user
    #         )
    #         return specialist_department.first().department.name
    #     except:
    #         return 'Department has not been found'
    

    
    
    
    
    
    


    
    
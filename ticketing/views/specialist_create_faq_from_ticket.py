from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin
from django.shortcuts import redirect


from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ticketing.forms.specialist_faq import FAQForm
from django.urls import reverse, reverse_lazy
from ticketing.models.faq import FAQ
from ticketing.models.users import User
from ticketing.models.departments import Department
from ticketing.models.specialist import SpecialistDepartment
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin



from ticketing.models import (
    Ticket,
    SpecialistInbox,
    SpecialistDepartment,
    Message,
)

class SpecialistCreateFAQFromTicketView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'specialist_create_faq_from_ticket.html'
    required_roles = ['SP']
    form_class = FAQForm

    def form_valid(self, form):

        form.custom_save(
            specialist=self.request.user,
            department=SpecialistDepartment.objects.get(
                specialist=self.request.user
            ).department,
            questions=form.cleaned_data['questions'],
            subsection=form.cleaned_data['subsection'],
            answer=form.cleaned_data['answer'],
        )
        return redirect('specialist_dashboard', ticket_type='personal')








    
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
    

    
    
    
    
    
    


    
    
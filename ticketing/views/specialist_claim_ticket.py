from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed
from django.shortcuts  import redirect


from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment, Message

@method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class SpecialistClaimTicketView(View):
    template_name = "specialist_claim_ticket.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        # CHECK IF THE TICKET WE ARE VIEWING CAN BE VIEWED BY SPECIALIST
        department = (SpecialistDepartment.objects.filter(specialist = user).first()).department
        ticket = Ticket.objects.filter(id =self.kwargs["pk"])
       
        return self.validate_view_ticket(user,department,ticket,request)

    def post(self, request, *args, **kwargs):
       
        ticket_id= self.request.POST.get('accept_ticket')
        ticket_list = Ticket.objects.filter(id = ticket_id)
        if(len(ticket_list) == 0):
            return render('/specialist_dashboard')
        
        else:
            SpecialistInbox.objects.create(
                specialist = request.user,
                ticket = ticket_list[0]
            )
        
        return redirect('/specialist_dashboard')

    def validate_view_ticket(self,user,department,ticket,request):
       
      
        if(len(ticket) > 0 and department == ticket[0].department):
            message = Message.objects.filter(ticket = ticket.first()).first()
            return render(request, self.template_name, {'ticket': ticket.first(), 'message' : message})   
        else:
        
            return redirect('/specialist_dashboard')

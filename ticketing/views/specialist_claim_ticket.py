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
        if(len(ticket)>0 and department == ticket[0].department):
            message = Message.objects.filter(ticket = ticket.first()).first()
            return render(request, self.template_name, {'ticket': ticket.first(), 'message' : message})
        
        else:
            return redirect('/specialist_dashboard')
        
    def post(self, request, *args, **kwargs):
        ticketID= self.request.POST.get('acceptTicket')
        ticketList = Ticket.objects.filter(id = ticketID)
        if(len(ticketList) == 0):
            return redirect('/specialist_dashboard')
        else:
            SpecialistInbox.objects.create(
                specialist = request.user,
                ticket = ticketList[0]
            )
        return redirect('/specialist_dashboard')


            
        



        



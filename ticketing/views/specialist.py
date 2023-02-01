from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed

from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment

@method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class SpecialistInboxView(ListView):
    model = Ticket
    template_name = 'specialist_dashboard.html'

    def get_queryset(self):
        type = self.request.POST.get('typeOfTicket')
        match type:
                case "department" : ticketlist = Ticket.objects.filter(department = SpecialistDepartment.objects.get(specialist = user).department)
                case "personal" : ticketlist = SpecialistInbox.objects.filter(specialist = user).only('ticket')
                case default : ticketlist = []
        return ticketlist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apple"] =  "apple"
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        ticketType = "department"
        ticketlist = Ticket.objects.filter(department = SpecialistDepartment.objects.get(specialist = user).department)
        return render(request, 'specialist_dashboard.html', {'object_list': ticketlist, "ticketType": ticketType})

    def post(self, request, *args, **kwargs):
        print(self.request.POST.get('view_ticket'))
        return SpecialistInboxView.as_view()(request)
    


# class DashboardView(View):
#     @method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), login_required)

#     def post(self, request, *args, **kwargs):

#         user = request.user
#         type = request.POST.get('typeOfTicket')
#         ticketType = type
        
#         match type:
#             case "department" : ticketlist = Ticket.objects.filter(department = SpecialistDepartment.objects.get(specialist = user).department)
#             case "personal" : ticketlist = SpecialistInbox.objects.filter(specialist = user).only('ticket')
#             #case "archived" :
#             case default : ticketlist = []

#         return render(request, 'specialist_dashboard.html', {'object_list': ticketlist, "ticketType": ticketType})

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ticketType = "personal"
#         ticketlist = SpecialistInbox.objects.filter(specialist = user).values_list('ticket')
#         return render(request, 'specialist_dashboard.html', {'object_list': ticketlist, "ticketType": ticketType})



    
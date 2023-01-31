from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required

from ticketing.models import Ticket, SpecialistInbox, SpecialistDepartment



class DashboardView(View):
    @method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), login_required)

    def post(self, request, *args, **kwargs):

        user = request.user
        
        type = request.POST.get('typeOfTicket')
        match type:
            case "department" : ticketlist = Ticket.objects.filter(department = SpecialistDepartment.objects.get(specialist = user).department)
            case "personal" : ticketlist = SpecialistInbox.objects.filter(specialist = user).only('ticket')
            #case "archived" :
            case default : ticketlist = []

        return render(request, 'specialist_db.html', {'object_list': ticketlist})

    def get(self, request, *args, **kwargs):
        user = request.user
        ticketlist = SpecialistInbox.objects.filter(specialist = user).values_list('ticket')
        return render(request, 'specialist_db.html', {'object_list': ticketlist} )

    
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from ticketing.models import * 

class StudentInboxView(ListView):  
    model = Ticket
    template_name = 'student_dashboard.html'
    paginate_by = 5  # if pagination is desired
    def get_queryset(self):
        tickets = Ticket.objects.filter(student_id = self.request.user.id)
        if self.request.method == "GET": # Gets all tickets from that user
            print("Jumped into get")
            return tickets
        
        if self.request.method == "POST":
            print("Jumped into post")
            ticketType = self.request.POST.get('typeOfTicket')
            match ticketType:
                case "Open":
                    return tickets.filter(status = "Open")
                case "Closed":
                    return tickets.filter(status = "Closed")
                case default:
                    return tickets
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticketType = ""
        if self.request.method == "POST":
            ticketType = self.request.POST.get('id')

        context["ticketType"] = ticketType
        return context

    def post(self, request, *args, **kwargs):
        return render(request,'student_dashboard.html', {
            'page_obj': self.get_queryset(),
            'ticketType': self.request.POST.get('typeOfTicket')
        })

# class StatusInboxView(ListView):
#     model = Ticket
#     template_name = 'status_inbox.html'
#     paginate_by = 5
#     slug_field = 'status'

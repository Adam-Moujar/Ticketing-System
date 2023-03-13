from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404
from ticketing.models import *
from django.shortcuts import render, redirect


class DirectorStatisticsView(ListView):
    # model = Department
    template_name = 'director_statistics.html'
    # paginate_by = 10
    # paginate_by=25
    # def get_queryset(self):
    #     return Department.objects.all()

    def get_queryset(self):
        user = self.request.user
        facts = [{"title": "Department Information",
                  "data": [{
                        "name": "Number of departments",
                        "value": self.get_number_of_departments()
                    },
                    {
                        "name": "Number of tickets",
                        "value": 0
                    },
                    {   
                        "name": "Department with most answered tickets",
                        "value": 0
            
                    },
                    ]
                   },
                   {
                        "title": "Department with least unanswered tikets",
                        "data": [
                            {
                                "name": "Most Recent Response",
                                "value": 0
                            },
                            {
                                "name": "Average Messages per Ticket",
                                "value": 0
                            }
                        ]

                   }
                   ]
        
        return facts
    
    def get_number_of_departments(self):
        return Department.objects.count()
    
    def get_name_of_department_with_most_answered_tickets(self):
        current_max_department = None
        max_count = 0
        for department in Department.objects.all():
            ticket_count = Ticket.objects.filter(department = department, status = Ticket.Status.CLOSED).count() 
            if(ticket_count > max_count):
                max_count = ticket_count
                current_max_department = department

        return current_max_department
    # def get_number_of_total_tickets_per_department(self):
    #     user = self.request.user
    #     department = self.get_department()
    #     return Ticket.objects.filter(department= department).count()
               
        
    # def get_department(self):
    #     user = self.request.user
    #     department = (
    #             SpecialistDepartment.objects.filter(specialist=user).first()
    #         ).department
    #     return department
    
    # def get_number_of_open_tickets(self):
    #     user = self.request.user
    #     department = self.get_department()
    #     return Ticket.objects.filter(department= department, status = Ticket.Status.OPEN).count()
    
    # def get_number_of_closed_tickets(self):
    #     user = self.request.user
    #     department = self.get_department()
    #     return Ticket.objects.filter(department= department, status = Ticket.Status.CLOSED).count()
    
    # def get_time_of_most_recent_response(self):
    #     user = self.request.user
    #     department = self.get_department()
    #     tickets = Ticket.objects.filter(department = department)

    #     message = Message.objects.filter(ticket__in = tickets).latest("date_time")

    #     return message.date_time
    
    # def get_average_messages_per_ticket(self):
    #     user = self.request.user
    #     department = self.get_department()
    #     tickets = Ticket.objects.filter(department = department)

    #     total_messages = 0

    #     for ticket in tickets:
    #         total_messages += Message.objects.filter(ticket = ticket).count()

    #     if len(tickets) != 0:
    #         return round(total_messages / len(tickets),2)
    #     else:
    #         return 0
from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404
from ticketing.models import *
from django.shortcuts import render, redirect
import sys
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from ticketing.mixins import RoleRequiredMixin


class DirectorStatisticsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    # model = Department
    template_name = 'director_statistics.html'
    required_roles = ['DI']
    # paginate_by = 10
    # paginate_by=25
    # def get_queryset(self):
    #     return Department.objects.all()

    def get_queryset(self):
        user = self.request.user
        facts = [{
                    "title": "Department Information",
                    "data": [
                            {
                                "name": "Number of departments",
                                "value": self.get_number_of_departments()
                            },
                            {
                                "name": "Number of tickets",
                                "value": self.get_total_number_of_tickets()
                            },
                            {   
                                "name": "Department with most answered tickets",
                                "value": self.get_name_of_department_with_most_answered_tickets()
                    
                            },
                            {
                                "name": "Department with most unanswered tickets",
                                "value": self.get_name_of_department_with_least_answered_tickets()
                            }   
                        ]
                   },
                   {
                        "title": "Specialist Information",
                        "data": [
                            {
                                "name": "Average response time",
                                "value": self.get_average_response_time()
                            },
                            {
                                "name": "Average Messages per Ticket",
                                "value": self.get_average_number_of_messages_per_ticket()
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
    
    def get_total_number_of_tickets(self):
        return Ticket.objects.all().count()
    
    def get_name_of_department_with_least_answered_tickets(self):
        current_min_department = None
        min_count = sys.maxsize
        for department in Department.objects.all():
            ticket_count = Ticket.objects.filter(department = department, status = Ticket.Status.OPEN).count() 
            if(ticket_count < min_count):
                min_count = ticket_count
                current_min_department = department
        
        return current_min_department
    
    def get_average_response_time(self):
        total_time = datetime.timedelta()
        counter = 0
        for ticket in Ticket.objects.all():
            messages = SpecialistMessage.objects.filter(ticket=ticket).order_by('-date_time')
            specialist_message = None
            if messages:
                counter += 1
                specialist_message = messages[0]
                student_message = StudentMessage.objects.filter(ticket=ticket).order_by('-date_time')[0]
                total_time += specialist_message.date_time - student_message.date_time
            
        if counter == 0:
            return "N/A"
        else:
            # return total_time / counter
            return total_time / counter
            # current_message = None

    def get_average_number_of_messages_per_ticket(self):
        number_of_tickets = Ticket.objects.count()
    
        number_of_messages = Message.objects.count()

        if number_of_tickets == 0:
            return 0
        else:
            return round(number_of_messages / number_of_tickets,2)
            
            # for message in messages:
        
            #     print("MSG CONTENT: ", message.content)
            #     if isinstance(message, SpecialistMessage):

                    
            #         current_message = message
            #         break

          
               

            # if current_message:
            #     time_diff =  current_message.date_time - messages[0].date_time
            #     print(time_diff)
             
            #     return time_diff
            
        

                


                    

    
    
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
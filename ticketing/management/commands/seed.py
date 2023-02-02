from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from ticketing.models import * 
from datetime import * 
from faker import Faker
import random

class Command(BaseCommand): 
    # constant
    DEPARTMENT = ['Cost of living' , 
                    'Student wellbeing' , 
                    'Fees, Funding & Money', 
                    'Immigration & visa advice', 
                    'Accommodation']
    STUDENT_COUNT = 100
    SPECIALIST_COUNT = 20
    DEPARTMENT_COUNT = len(DEPARTMENT)
    DIRECTOR_COUNT = 3
    PASSWORD = 'Password@123'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options ):

        self.create_student()
        print('students done') 
        
        self.create_specialist()
        print('specialist done')
        
        self.create_director()
        print('directors done')
        
        self.create_department()
        print('department done')
        
        self.create_specialist_department()
        print('specialist set to department')
        
        self.create_student_ticket()
        print('student ticket done')

        self.create_specialist_indox()
        print('specialist inbox done')

    def set_up(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = (f'{first_name}.{last_name}@example.com').lower()

        return [first_name, last_name, email]

    def create_student(self):   
        for _ in range(self.STUDENT_COUNT):
            info = self.set_up()
            User.objects.create_user(email = info[2],
                                    password = self.PASSWORD, 
                                    first_name = info[0], 
                                    last_name = info[1])
   
    def create_specialist(self):
        for _ in range(self.SPECIALIST_COUNT):
            info = self.set_up()
            User.objects.create_specialist_user(email = info[2], 
                                    password = self.PASSWORD, 
                                    first_name = info[0], 
                                    last_name = info[1])
    
    def create_director(self): 
         for i in range(self.DIRECTOR_COUNT):
            info = self.set_up()
            User.objects.create_superuser(email = info[2], 
                                    password = self.PASSWORD, 
                                    first_name = info[0], 
                                    last_name = info[1])

    def create_department(self): 
        for dep_name in self.DEPARTMENT: 
            Department.objects.create(name = dep_name)

    def create_student_ticket(self):
        for student in User.objects.filter(role = User.Role.STUDENT):
            department_obj_list = Department.objects.all()
            rand_dep = department_obj_list[random.randint(0, self.DEPARTMENT_COUNT - 1)]
            ticket = Ticket.objects.create(student = student, 
                                        department = rand_dep,
                                        header = self.faker.sentence()[0 : 100])
            self.create_student_message(ticket)

    def create_student_message(self, ticket):
        StudentMessage.objects.create(ticket = ticket,
                                    content = self.faker.text()[0 : 500])

    def create_specialist_department(self): 
        for specialist in User.objects.filter(role = User.Role.SPECIALIST) : 
            department_list = Department.objects.all()
            rand_dep = department_list[random.randint(0, self.DEPARTMENT_COUNT - 1)]
            SpecialistDepartment.objects.create(specialist = specialist, department = rand_dep)
            
    def create_specialist_indox(self):
        for department in Department.objects.all():
            specialists = User.objects.filter(id__in = SpecialistDepartment.objects.filter(department = department).values_list('specialist', flat = True))
            tickets = Ticket.objects.filter(department = department)
            for ticket in tickets:
                rand_specialist = specialists[random.randint(0, len(specialists) - 1)]
                specialist_ticket = SpecialistInbox.objects.create(specialist = rand_specialist, ticket = ticket)
                self.create_specialist_message(specialist_ticket)
        
    def create_specialist_message(self, specialist_ticket):
        SpecialistMessage.objects.create(ticket = specialist_ticket.ticket, 
                                    content = self.faker.text()[0 : 500], 
                                    responder = specialist_ticket.specialist)
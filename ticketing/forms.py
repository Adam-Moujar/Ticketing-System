from ticketing.models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs = {'class': 'form-control', 'id': 'email', 'placeholder': 'Email'})
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class': 'form-control', 'id': 'password', 'placeholder': 'Password'})
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class StudentTicketForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=500)
    def custom_save(self, student, department, header, content): 
        ticket = Ticket.objects.create(student = student, 
                                    department = department, 
                                    header = header)
        StudentMessage.objects.create(ticket = ticket, 
                                    content = content)


    class Meta: 
        model = Ticket
        fields = ['header', 'department']


# class DepartmentAddForm(forms.ModelForm):
#     name = 
#     class Meta:
#         model = Department
#         fields = "__all__"

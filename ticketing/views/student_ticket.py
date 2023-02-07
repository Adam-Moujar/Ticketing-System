from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from ticketing.forms import StudentTicketForm
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
from ticketing.models import * 

@method_decorator(roles_allowed(allowed_roles = ['ST']), name='dispatch') # Ticket and Message
@method_decorator(login_required, name='dispatch')
class StudentTicketView(FormView):
    template_name = 'student_ticket_form.html'
    form_class = StudentTicketForm
    success_url = reverse_lazy('student_dashboard')
    
    
    def form_valid(self, form):
        student = User.objects.get(id=self.request.user.id)

        form.custom_save(student = student, 
                        department = form.cleaned_data['department'], 
                        header = form.cleaned_data['header'],
                        content = form.cleaned_data['content'])
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, **kwargs):
        print(form.errors.as_data())
        return self.render_to_response(self.get_context_data())
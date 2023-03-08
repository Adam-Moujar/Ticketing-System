from ticketing.models import *
from django.views.generic import DetailView

class StudentMessageView(DetailView):
    model = Ticket
    template_name = "student_message.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(ticket=self.object)
        return context

from ticketing.models import Message, Ticket, StudentMessage, SpecialistMessage
from django.views.generic import DetailView, ListView
from itertools import chain
from operator import attrgetter

# class StudentMessageView(DetailView):
#     model = Ticket
#     template_name = "student_message.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['messages'] = Message.objects.filter(ticket=self.object)
#         return context


class StudentMessageView(ListView):
    model = SpecialistMessage
    template_name = 'student_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        student_message = StudentMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        specialist_message = SpecialistMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        queryset = sorted(
            chain(student_message, specialist_message),
            key=attrgetter('date_time'),
        )
        return queryset

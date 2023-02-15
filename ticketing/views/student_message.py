from ticketing.mixins import RoleRequiredMixin
from ticketing.models import Message, Ticket, StudentMessage, SpecialistMessage
from django.views.generic import DetailView, ListView, CreateView
from itertools import chain
from operator import attrgetter
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentMessageView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = StudentMessage
    template_name = 'student_message.html'
    fields = ['content']
    required_roles = ['ST', 'SP']

    def dispatch(self, request, *args, **kwargs):
        allowed_ids = []
        # TODO move this to a helper class
        allowed_ids.append(
            getattr(
                getattr(Ticket.objects.get(id=self.kwargs['pk']), 'student'),
                'id',
            )
        )
        if self.request.user.id not in allowed_ids:
            return HttpResponseRedirect(reverse('student_dashboard'))
        print(self.request.user.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id=self.kwargs['pk'])
        student_message = StudentMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        specialist_message = SpecialistMessage.objects.filter(
            ticket=self.kwargs['pk']
        )
        context['message_list'] = sorted(
            chain(student_message, specialist_message),
            key=attrgetter('date_time'),
        )
        return context

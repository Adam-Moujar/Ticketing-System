from ticketing.mixins import RoleRequiredMixin
from ticketing.models import (
    Message,
    Ticket,
    StudentMessage,
    SpecialistMessage,
    SpecialistDepartment,
)
from django.views.generic import DetailView, ListView, CreateView
from itertools import chain
from operator import attrgetter
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SpecialistMessageView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = SpecialistMessage
    template_name = 'specialist_message.html'
    fields = ['content']
    required_roles = ['SP']

    def dispatch(self, request, *args, **kwargs):
        # TODO add all specialists ids to this
        # TODO move this to a helper class
        department = getattr(
            Ticket.objects.get(id=self.kwargs['pk']), 'department'
        )
        allowed_ids = SpecialistDepartment.objects.filter(
            department=department
        ).values_list('specialist', flat=True)
        # allowed_ids = getattr(getattr(Ticket.objects.filter(id=self.kwargs['pk']), 'department'), 'id')
        if self.request.user.id not in allowed_ids:
            return HttpResponseRedirect(reverse('specialist_dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        self.object.responder = self.request.user
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

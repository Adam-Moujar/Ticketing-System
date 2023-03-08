from django.shortcuts import render

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


class MessageListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Message
    template_name = 'partials/message_list.html'
    required_roles = ['ST', 'SP']
    # paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        allowed_ids = list(
            SpecialistDepartment.objects.filter(
                department=getattr(
                    Ticket.objects.get(id=self.kwargs['pk']), 'department'
                )
            ).values_list('specialist', flat=True)
        )
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
            reverse=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id=self.kwargs['pk'])
        return context

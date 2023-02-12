from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from ticketing.models.faq import FAQ
from ticketing.models.departments import Department


class DepartmentFAQ(ListView):
    model = FAQ
    template_name = 'department_faq.html'
    paginate_by = 25

    def get_queryset(self):
        return FAQ.objects.filter(department__slug=self.kwargs['department'])

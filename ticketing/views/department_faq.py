from django.contrib.auth.decorators import login_required
from ticketing.decorators import roles_allowed
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from ticketing.models.faq import FAQ


class DepartmentFAQ(ListView):
    model = FAQ
    template_name = 'department_faq.html'
    paginate_by = 25

    def get_object(self):
        return get_object_or_404(FAQ, slug=self.kwargs['slug'])

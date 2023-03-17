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
        queryset = FAQ.objects.filter(
            department__slug=self.kwargs['department']
        )
        queryset = queryset.order_by('question')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = get_object_or_404(
            Department, slug=self.kwargs['department']
        )
        if department:
             context['department_name'] = department.name
        else:
            context['department_name']=''
            
        faqs=FAQ.objects.filter(department=department)
        faq_dict={}
        for faq in faqs:
            if faq.subsection not in faq_dict:
                faq_dict[faq.subsection]=[]
            faq_dict[faq.subsection].append(faq)
        context['faq_dict']=faq_dict
            
        return context

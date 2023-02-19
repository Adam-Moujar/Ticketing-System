from ticketing.models import User, Department
from ticketing.utility.error_messages import *
from ticketing.views.utility.mixins import ExtendableFormViewMixin
from ticketing.forms2.department import DepartmentFilterForm

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from ticketing.forms import *
from django.views.generic.edit import CreateView
from ticketing.mixins import RoleRequiredMixin
from ticketing.utility.user import *
from django.contrib.auth.mixins import LoginRequiredMixin


def delete_department(id):
    try:
        department = Department.objects.get(id=id)

        department.delete()

        return True

    except Department.DoesNotExist:
        return False


class DepartmentManagerView(
    LoginRequiredMixin,
    RoleRequiredMixin,
    ExtendableFormViewMixin,
    CreateView,
    ListView,
):
    required_roles = [User.Role.DIRECTOR]

    paginate_by = 10
    model = Department
    fields = ['name']
    success_url = reverse_lazy('department_manager')

    def setup(self, request):

        super().setup(request)

        self.filter_form = DepartmentFilterForm(request.GET)

        self.result = self.filter_form.is_valid()

        self.get_name = self.filter_form.cleaned_data.get('name')

    def get_queryset(self):
        return Department.objects.filter(name__istartswith=self.get_name)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({'filter_form': self.filter_form})

        return context

    def post(self, request, *args, **kwargs):

        super().get(request)

        edit_id = request.POST.get('edit')
        delete_id = request.POST.get('delete')

        if request.POST.get('add'):
            return super().post(request, *args, **kwargs)

        elif edit_id:
            response = redirect('edit_department', pk=edit_id)

            return response

        elif delete_id:
            result = delete_department(delete_id)

            if result == False:
                messages.add_message(
                    request, messages.ERROR, USER_NO_EXIST_MESSAGE
                )

        elif request.POST.get('reset'):
            return redirect('department_manager')

        return self.fixed_post(request, *args, **kwargs)

    def get_template_names(self):
        return ['department_manager.html']

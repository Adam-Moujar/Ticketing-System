from ticketing.models import User, Department
from ticketing.utility.error_messages import *
from ticketing.views.utility.mixins import ExtendableFormViewMixin

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


def delete_department(id):
    try:
        department = Department.objects.get(id=id)

        department.delete()

        return True

    except Department.DoesNotExist:
        return False


class DepartmentManagerView(
    RoleRequiredMixin, ExtendableFormViewMixin, CreateView, ListView
):
    required_roles = [User.Role.DIRECTOR]

    paginate_by = 10
    model = Department
    fields = ['name']
    success_url = reverse_lazy('department_manager')

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

        return self.fixed_post(request, *args, **kwargs)

    def get_template_names(self):
        return ['department_manager.html']

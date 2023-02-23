from ticketing.forms2.director_panel import (
    DirectorFilterForm,
    DirectorCommandsForm,
    make_add_user_form_class,
)
from ticketing.models import User, Department, SpecialistDepartment
from ticketing.utility.error_messages import *
from ticketing.forms import SignupForm
from ticketing.views.utility.mixins import (
    ExtendableFormViewMixin,
    DynamicCustomFormClassMixin,
    FilterView,
)

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import CreateView
from ticketing.mixins import RoleRequiredMixin
from ticketing.utility.model import *
from ticketing.utility.user import *
from django.contrib.auth.mixins import LoginRequiredMixin


def set_multiple_users_role(users, user_role, department_id):
    problem_occured = False

    for user in users:
        try:
            id = int(user)
            user = User.objects.get(id=id)

            department = get_model_object(Department, id=department_id)

            update_specialist_department(
                user, user.role, user_role, department
            )

            # print("OLD ROLE: ", user.role, " NEW ROLE: ", user_role)

            user.role = user_role

            user.save()

        except User.DoesNotExist:
            problem_occured = True

        except ValueError:
            problem_occured = True

    return not problem_occured


def delete_users(user_id_strings):
    problem_occured = False

    for id_str in user_id_strings:
        try:
            id = int(id_str)
            user = User.objects.get(id=id)

            if user.role == User.Role.SPECIALIST:
                delete_model_object(SpecialistDepartment, specialist=id)

            user.delete()

        except User.DoesNotExist:
            problem_occured = True

        except ValueError:
            problem_occured = True

    return not problem_occured


class DirectorPanelView(
    LoginRequiredMixin,
    RoleRequiredMixin,
    ExtendableFormViewMixin,
    DynamicCustomFormClassMixin,
    FilterView,
    CreateView,
    ListView,
):

    required_roles = [User.Role.DIRECTOR]

    paginate_by = 10
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('director_panel')

    form_class_maker = make_add_user_form_class

    filter_form_class = DirectorFilterForm
    filter_reset_url = 'director_panel'

    def setup(self, request):

        super().setup(request)

        self.error = False

        self.commands_form = None
        self.selected = []

    def get_queryset(self):

        users = User.objects.filter(
            email__istartswith=self.filter_data['email'],
            first_name__istartswith=self.filter_data['first_name'],
            last_name__istartswith=self.filter_data['last_name'],
        )

        if self.filter_data['id']:
            users = users.filter(id__exact=self.filter_data['id'])

        if self.filter_data['filter_role']:
            users = users.filter(role__exact=self.filter_data['filter_role'])

        if self.filter_data['filter_department']:
            users = users.filter(
                id__in=SpecialistDepartment.objects.filter(
                    department=self.filter_data['filter_department']
                ).values_list('specialist', flat=True)
            )

        return users

    def get_template_names(self):
        return ['director_panel.html']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.commands_form == None:
            self.commands_form = DirectorCommandsForm()

        if self.error == False:
            self.selected = []

        context.update(
            {
                'commands_form': self.commands_form,
                'selected': self.selected,
            }
        )

        return context

    def post(self, request):

        super().get(request)

        self.selected = request.POST.getlist('select')
        edit_id = request.POST.get('edit')

        if edit_id:
            request.session['director_panel_query'] = request.GET.urlencode()

            response = redirect('edit_user', pk=edit_id)

            return response

        elif request.POST.get('add'):
            return super().post(request)

        elif request.POST.get('password'):

            change_id = request.POST.get('password')

            request.session['director_panel_query'] = request.GET.urlencode()

            response = redirect('change_password', pk=change_id)

            return response

        if len(self.selected) == 0:
            # Remaining possible POST requests rely on there being users selected
            self.error = True
            messages.add_message(
                request, messages.ERROR, 'No users have been selected'
            )

            return self.fixed_post(request)

        if request.POST.get('set_role'):

            role = request.POST.get('commands_role')
            department = request.POST.get('commands_department')

            self.commands_form = DirectorCommandsForm(request.POST)

            if not self.commands_form.is_valid():
                self.error = True
                messages.add_message(
                    request, messages.ERROR, 'Your command failed'
                )

                return self.fixed_post(request)

            elif not role:
                self.error = True
                messages.add_message(
                    request,
                    messages.ERROR,
                    'You have not selected a role for the user',
                )

                return self.fixed_post(request)

            if role != User.Role.SPECIALIST:
                department = None

            result = set_multiple_users_role(self.selected, role, department)

            if result == False:
                self.error = True
                messages.add_message(
                    request, messages.ERROR, USER_NO_EXIST_MESSAGE
                )

        elif request.POST.get('delete'):

            result = delete_users(self.selected)

            if result == False:
                self.error = True
                messages.add_message(
                    request, messages.ERROR, USER_NO_EXIST_MESSAGE
                )

        return self.fixed_post(request)

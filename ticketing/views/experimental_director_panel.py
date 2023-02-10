from ticketing.forms2.director_panel import DirectorFilterForm, DirectorCommandsForm, make_add_user_form_class
from ticketing.models import User, Department
from ticketing.utility.error_messages import *
from ticketing.forms import SignupForm
from ticketing.views.utility.mixins import ExtendableFormViewMixin, DynamicCustomFormClassMixin

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import CreateView


def add_user(user, role, department):
    user.password = make_password(user.password)
    user.role = role

    if(role == User.Role.SPECIALIST):
        SpecialistDepartment(specialist = user, department = department).save()


    user.save()

def validate_role(role):
    valid_roles = [User.Role.STUDENT, User.Role.SPECIALIST, User.Role.DIRECTOR]

    if(role not in valid_roles):
        return False
    
    return True

def set_multiple_users_role(users, user_role):
    problem_occured = False

    for user in users:
        try:
            id = int(user)
            user = User.objects.get(id = id)
            
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
            user = User.objects.get(id = id)

            user.delete()

        except  User.DoesNotExist:
            problem_occured = True

    return not problem_occured


class DirectorPanelView(ExtendableFormViewMixin, DynamicCustomFormClassMixin, CreateView, ListView):

    paginate_by = 10
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("department_manager")

    form_class_maker = make_add_user_form_class


    # def custom_get_form_kwargs(self):
    #     _kwargs = super().get_form_kwargs()

    #     _kwargs.pop("data", None)
    #     _kwargs.pop("files", None)

    #     return _kwargs

    def setup(self, request):

        print("WE ARE ABOVE SETUP")

        super().setup(request)

        self.error = ""

        self.filter_form = DirectorFilterForm(request.GET)
        #self.add_user_form = AddUserForm()

        self.result = self.filter_form.is_valid()

        self.get_id = self.filter_form.cleaned_data.get("id")
        self.get_first_name = self.filter_form.cleaned_data.get("first_name", "")
        self.get_last_name = self.filter_form.cleaned_data.get("last_name", "")
        self.get_email = self.filter_form.cleaned_data.get("email", "")
        self.get_role = self.filter_form.cleaned_data.get("role")

        #print("FILTER FORM IS: ", self.filter_form)

    
    def get_queryset(self):

        users = User.objects.filter(email__istartswith = self.get_email,
                                   first_name__istartswith = self.get_first_name,
                                   last_name__istartswith = self.get_last_name)

        if self.get_id:
            users = users.filter(id__exact = self.get_id)

        if self.get_role:
            users = users.filter(role__exact = self.get_role)

        return users


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({"commands_form": DirectorCommandsForm(),
                        "filter_form": self.filter_form})

        return context


    # def get(self, request):

    #     print("")
        
    #     self.setup(request)

    #     return super().get(request)

    #     #return self.end(request)

    def post(self, request):
        #self.start(request)

        super().get(request)

        selected = request.POST.getlist('select')
        edit_id = request.POST.get('edit')

        if edit_id:
            request.session["director_panel_query"] = request.GET.urlencode()

            response = redirect("experimental_edit_user", pk = edit_id)
            # response['Location'] += '?id=' + edit_id
            return response

        elif request.POST.get('add'):
            # self.add_user_form = AddUserForm(request.POST)

            # if not self.add_user_form.is_valid():
            #     return self.end(request)

            # user = self.add_user_form.save(commit = False)

            # add_user(user, self.add_user_form.cleaned_data.get("add_user_role"), 
            #             self.add_user_form.cleaned_data.get("add_user_department"))

            # self.add_user_form = AddUserForm()

            return super().post(request)
        
        elif request.POST.get('reset'):
            return redirect("director_panel")

        elif request.POST.get('password'):

            change_id = request.POST.get('password')

            request.session["director_panel_query"] = request.GET.urlencode()

            response = redirect("change_password")
            response['Location'] += '?id=' + change_id

            return response

        #print("LEN SELECTED IS: ", len(selected))
        if len(selected) == 0:
            # Remaining possible POST requests rely on there being users selected
            self.error = "No users have been selected"

            return self.fixed_post(request)

        if request.POST.get('set_role'):

            role = request.POST.get('commands_role')
            if not role:
                self.error = "You have not selected a role for the user"

                return self.fixed_post(request)

            if not validate_role(role):
                self.error = "Invalid user role selected"

                return self.fixed_post(request)

            result = set_multiple_users_role(selected, role)

            if result == False:
                self.error = USER_NO_EXIST_MESSAGE

        elif request.POST.get('delete'):

            result = delete_users(selected)

            if result == False:
                self.error = USER_NO_EXIST_MESSAGE

        return self.fixed_post(request)


    # def post_end(self, request):

    #     old_get_form_kwargs = self.get_form_kwargs
    #     self.get_form_kwargs = self.custom_get_form_kwargs

    #     result = super().post(request, *args, **kwargs)

    #     self.get_form_kwargs = old_get_form_kwargs

        return result

    def get_template_names(self):
        return ["director_panel.html"]

    # def end(self, request):

    #     self.context.update(super().get(request).context_data)

    #     if len(self.error) > 0:
    #         messages.add_message(request, messages.ERROR, self.error)


    #     self.context.update({"error" : self.error,
    #                "form": self.form,
    #                "commands_form": DirectorCommandsForm(),
    #                "add_user_form": self.add_user_form})

    #     return render(request, "director_panel.html", self.context)



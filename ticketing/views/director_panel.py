from ticketing.forms2.director_panel import DirectorFilterForm, DirectorCommandsForm, AddUserForm
from ticketing.models import User

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def add_user(user, role):
    user.password = make_password(user.password)

    user.role = role

    user.save()

def validate_role(role):
    valid_roles = [User.Role.STUDENT, User.Role.SPECIALIST, User.Role.DIRECTOR]

    if(role not in valid_roles):
        return False
    
    return True

def set_multiple_users_role(users, user_role):
    wasProblem = False

    print("users are: ", users)
    for user in users:
        try:
            id = int(user)
            user = User.objects.get(id = id)

            user.role = user_role

            user.save()

        except User.DoesNotExist:
            wasProblem = True

        except ValueError:
            wasProblem = True

    return not wasProblem


def delete_users(user_id_strings):
    wasNonExistentUser = False

    for id_str in user_id_strings:
        try:
            id = int(id_str)
            user = User.objects.get(id = id)

            user.delete()

        except  User.DoesNotExist:

            wasNonExistentUser = True

    return not wasNonExistentUser


class DirectorPanelView(ListView):

    paginate_by = 10
    #context_object_name = 'page_obj'
    #queryset = User.objects.all()
    model = User

    NON_EXISTENT_USER_MSG = "One or more of the selected users did not exist"

    #def get_queryset(self):
        #print("ABOUT TO RETURN: " + User.objects.all())
     #   return User.objects.all()

    def start(self, request):
        self.error_str = ""

        self.form = DirectorFilterForm(request.GET)
        self.add_user_form = AddUserForm()

        # Even if the form contains some invalid input we want to continue
        # with what valid inputs we have.
        self.result = self.form.is_valid()

        self.get_id = self.form.cleaned_data.get("id")
        self.get_first_name = self.form.cleaned_data.get("first_name", "")
        self.get_last_name = self.form.cleaned_data.get("last_name", "")
        self.get_email = self.form.cleaned_data.get("email", "")
        self.get_role = self.form.cleaned_data.get("account_role")
        


    def get(self, request):
        #print("WE ARE IN GET")
        self.context = super().get(request).context_data

        self.start(request)

        return self.end(request)



    def post(self, request):
        self.start(request)

        selected = request.POST.getlist('select')
        edit_id = request.POST.get('edit')

        if edit_id:
            request.session["director_panel_get_query"] = request.GET.urlencode()

            response = redirect("edit_user")
            response['Location'] += '?id=' + edit_id
            return response

        elif request.POST.get('reset'):
            # Redirect without any GET query headers
            return redirect("director_panel")

        elif request.POST.get('add'):
            self.add_user_form = AddUserForm(request.POST)

            if not self.add_user_form.is_valid():
                return self.end(request)

            user = self.add_user_form.save(commit = False)

            add_user(user, self.add_user_form.cleaned_data.get("add_user_account_role"))

            self.add_user_form = AddUserForm()

            return self.end(request)


        change_id = request.POST.get('password')
        if change_id:
            request.session["director_panel_get_query"] = request.GET.urlencode()

            response = redirect("change_password")
            response['Location'] += '?id=' + change_id
            return response

        print("LEN SELECTED IS: ", len(selected))
        if len(selected) == 0:
            # Remaining possible POST requests rely on there being users selected
            self.error_str = "No users have been selected"

            return self.end(request)

        if request.POST.get('set_account_role'):

            role = request.POST.get('commands_account_role')
            if not role:
                self.error_str = "You have not selected an account role"

                return self.end(request)

            if not validate_role(role):
                self.error_str = "Invalid account type selected"

                return self.end(request)

            print(selected)
            result = set_multiple_users_role(selected, role)

            if result == False:
                self.error_str = self.NON_EXISTENT_USER_MSG

        elif request.POST.get('delete'):

            result = delete_users(selected)

            if result == False:
                self.error_str = self.NON_EXISTENT_USER_MSG

        return self.end(request)


    def end(self, request):

        users = User.objects.filter(email__istartswith = self.get_email,
                                   first_name__istartswith = self.get_first_name,
                                   last_name__istartswith = self.get_last_name)

        # We filter ID and account type exactly so we must make sure
        # they have a value before filtering.
        if self.get_id:
            users = users.filter(id__exact = self.get_id)

        if self.get_role:
            users = users.filter(role__exact = self.get_role)

        if len(self.error_str) > 0:
            messages.add_message(request, messages.ERROR, self.error_str)


        self.context.update({"error_str" : self.error_str,
                   "users" : users,
                   "form": self.form,
                   "commands_form": DirectorCommandsForm(),
                   "add_user_form": self.add_user_form})

        return render(request, "director_panel.html", self.context)



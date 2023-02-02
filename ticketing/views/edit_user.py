from ticketing.forms2.edit_user import EditUserForm
from ticketing.models import User
from ticketing.utility import get
from ticketing.utility.get import get_user_from_id_param

from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def update_user(user, first_name, last_name, email, role):
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.role = role

    user.save()


class EditUserView(View):

    error = ""

    def handle_id_param_error(self, request, error):
        return render(request, "edit_user.html", {"error" : error})
    
    def start(self, request, user = None):

        self.user = user

        self.form = EditUserForm(user = user,
                        initial = {"update_email" : user.email,
                                    "first_name" : user.first_name,
                                    "last_name": user.last_name,
                                    "edit_account_role": user.role})


    @get_user_from_id_param(handle_id_param_error)
    def get(self, request, user = None):
        self.start(request, user)

        return self.end(request)


    @get_user_from_id_param(handle_id_param_error)
    def post(self, request, user = None):
        self.start(request, user)

        if request.POST.get("save"):
            self.form = EditUserForm(request.POST, user = self.user)

            if not self.form.is_valid():
                return self.end(request)

            first_name = self.form.cleaned_data["first_name"]
            last_name = self.form.cleaned_data["last_name"]
            email = self.form.cleaned_data["update_email"]
            account_role = self.form.cleaned_data["edit_account_role"]

            update_user(self.user, first_name, last_name, email, account_role)

            return get.redirect_to_director_panel_with_saved_params(request)

        elif request.POST.get("cancel"):
            return get.redirect_to_director_panel_with_saved_params(request)

        return self.end(request)


    def end(self, request):
        if len(self.error) > 0:
            messages.add_message(request, messages.ERROR, self.error)

        return render(request, "edit_user.html", {"id" : request.GET.get("id"),
                                                  "user" : self.user,
                                                  "form" : self.form,
                                                  "error" : self.error})



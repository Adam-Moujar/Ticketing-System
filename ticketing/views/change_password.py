from ticketing.forms2.change_password import ChangePasswordForm
from ticketing.models import User
from ticketing.utility import get
#from ticketing.utility.user import get_user
from ticketing.utility.get import get_user_from_id_param

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def change_password(user, new_password):
    user.password = make_password(new_password)
    
    user.save()


class ChangePasswordView(View):

    PERMISSION_MSG = "You do not have permission to do this"

    error_str = ""

    def handle_id_param_error(self, request, error_str):
        print("ERROR_STR IS ", error_str)
        return render(request, "change_password.html", {"error_str" : error_str})


    def start(self, request, user = None):

        self.user = user

        self.form = ChangePasswordForm()

        print("USER IS ", request.user.is_anonymous)
        if request.user.is_anonymous or (request.user.role != User.Role.DIRECTOR and self.user.id != request.user.id):
            print("SHOULD BE IN HERE")
            return self.handle_id_param_error(request, self.PERMISSION_MSG)

            print("WE GET AFRTER???")

    @get_user_from_id_param(handle_id_param_error)
    def get(self, request, user = None):
        self.start(request, user)

        return self.end(request)


    @get_user_from_id_param(handle_id_param_error)
    def post(self, request, user = None):
        self.start(request, user)

        if request.POST.get("change"):
            self.form = ChangePasswordForm(request.POST)

            if not self.form.is_valid():
                return self.end(request)

            password = self.form.cleaned_data["password"]

            change_password(self.user, password)

            return get.redirect_to_director_panel_with_saved_params(request)

        elif request.POST.get("cancel"):
            return get.redirect_to_director_panel_with_saved_params(request)

        return self.end(request)


    def end(self, request):
        if len(self.error_str) > 0:
            messages.add_message(request, messages.ERROR, self.error_str)

        return render(request, "change_password.html", {"id" : request.GET.get("id"),
                                                  "user" : self.user,
                                                  "form" : self.form,
                                                  "error_str" : self.error_str})




        





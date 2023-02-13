from ticketing.forms2.change_password import ChangePasswordForm
from ticketing.models import User
from ticketing.utility import get
from ticketing.utility.get import get_user_from_id_param

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import UpdateView


def change_password(user, new_password):
    user.password = make_password(new_password)
    
    user.save()

class ChangePasswordView(UpdateView):

    PERMISSION_MESSAGE = "You must be a director to change other user's passwords"

    error = ""

    model = User
    form_class = ChangePasswordForm

    success_url = reverse_lazy("director_panel") # LATER - Change this depending on who is accessing


    def get_template_names(self):
        return ["edit_user.html"]


    def post(self, request, *args, **kwargs):

        if request.POST.get("cancel"):
            return get.redirect_to_director_panel_with_saved_params(request)

        return super().post(request, *args, **kwargs)



    def setup(self, request):

        self.user = user

        self.form = ChangePasswordForm()

        if request.user.is_anonymous or (request.user.role != User.Role.DIRECTOR and self.user.id != request.user.id):
            self.error = PERMISSION_MESSAGE

            # FIX THIS LATER

            return super().get(request)



    #@get_user_from_id_param(handle_id_param_error)
    def post(self, request):
        #self.start(request, user)

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
        if len(self.error) > 0:
            messages.add_message(request, messages.ERROR, self.error)

        return render(request, "change_password.html", {"id" : request.GET.get("id"),
                                                        "user" : self.user,
                                                        "form" : self.form,
                                                        "error" : self.error})


# class ChangePasswordView(View):

#     PERMISSION_MESSAGE = "You must be a director to change other user's passwords"

#     error = ""

#     def handle_id_param_error(self, request, error):
#         return render(request, "change_password.html", {"error" : error})


#     def start(self, request, user = None):

#         self.user = user

#         self.form = ChangePasswordForm()

#         if request.user.is_anonymous or (request.user.role != User.Role.DIRECTOR and self.user.id != request.user.id):
#             return self.handle_id_param_error(request, self.PERMISSION_MESSAGE)


#     @get_user_from_id_param(handle_id_param_error)
#     def get(self, request, user = None):
#         self.start(request, user)

#         return self.end(request)


#     @get_user_from_id_param(handle_id_param_error)
#     def post(self, request, user = None):
#         self.start(request, user)

#         if request.POST.get("change"):
#             self.form = ChangePasswordForm(request.POST)

#             if not self.form.is_valid():
#                 return self.end(request)

#             password = self.form.cleaned_data["password"]

#             change_password(self.user, password)

#             return get.redirect_to_director_panel_with_saved_params(request)

#         elif request.POST.get("cancel"):
#             return get.redirect_to_director_panel_with_saved_params(request)

#         return self.end(request)


#     def end(self, request):
#         if len(self.error) > 0:
#             messages.add_message(request, messages.ERROR, self.error)

#         return render(request, "change_password.html", {"id" : request.GET.get("id"),
#                                                         "user" : self.user,
#                                                         "form" : self.form,
#                                                         "error" : self.error})





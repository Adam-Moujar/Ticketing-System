from ticketing.forms2.change_password import ChangePasswordForm
from ticketing.models.users import User
from ticketing.utility import get
from ticketing.utility.get import get_user_from_id_param
from ticketing.mixins import RoleRequiredMixin

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import UpdateView, FormView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import PasswordChangeView


def change_password(user, new_password):
    user.password = make_password(new_password)

    user.save()


class ChangePasswordView(RoleRequiredMixin, FormView):

    required_roles = [
        User.Role.DIRECTOR,
        User.Role.SPECIALIST,
        User.Role.STUDENT,
    ]

    PERMISSION_MESSAGE = (
        "You must be a director to change other user's passwords"
    )

    error = ''

    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        _kwargs = super().get_form_kwargs()

        _kwargs.update({'user': self.user})

        return _kwargs

    def get_template_names(self):
        return ['change_password.html']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({'user': self.user})

        return context

    def setup(self, request, pk):

        try:
            self.user = User.objects.get(pk=pk)

        except User.DoesNotExist:
            raise Http404('No user found matching the query')

        if request.user.is_anonymous or (
            request.user.role != User.Role.DIRECTOR
            and self.user.id != request.user.id
        ):
            raise PermissionDenied

        super().setup(request, pk=pk)

    def post(self, request, pk):

        if request.POST.get('change'):
            self.form = ChangePasswordForm(request.POST, user=self.user)

            if not self.form.is_valid():
                return super().post(request, pk=pk)

            password = self.form.cleaned_data['password']

            change_password(self.user, password)

            return get.redirect_to_director_panel_with_saved_params(request)

        elif request.POST.get('cancel'):
            return get.redirect_to_director_panel_with_saved_params(request)

        return super().post(request, pk=pk)

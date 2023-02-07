from ticketing.forms2.director_panel import DirectorFilterForm, DirectorCommandsForm, AddUserForm
from ticketing.models import User, Department
from ticketing.utility.error_messages import *

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from ticketing.forms import *
from django.views.generic.edit import CreateView

def delete_department(id):
    try:
        department = Department.objects.get(id = id)

        department.delete()

        return True

    except  Department.DoesNotExist:
        return False

class DepartmentManagerView(CreateView, ListView):
    paginate_by = 10
    model = Department
    fields = ['name']
    success_url = reverse_lazy("department_manager")

    def custom_get_form_kwargs(self):
        _kwargs = super().get_form_kwargs()

        print("GOT KWARGS: THE DATA IS: ", _kwargs)

        _kwargs.pop("data", None)
        _kwargs.pop("files", None)

        print("GOT KWARGS: THE DATA AFTERRRRR IS: ", _kwargs)

        return _kwargs

    def post(self, request, *args, **kwargs):

        #print("FORM ERRORS AT THE MOST START: ", self.get_form().errors)

        super().get(request)

        edit_id = request.POST.get('edit')
        delete_id = request.POST.get('delete')

        if request.POST.get('add'):
            return super().post(request, *args, **kwargs)

        elif edit_id:
            response = redirect("edit_department", pk = edit_id)
            #response['Location'] += '?id=' + edit_id

            return response

        elif delete_id:
            result = delete_department(delete_id)

            if result == False:
                messages.add_message(request, messages.ERROR, USER_NO_EXIST_MESSAGE)


        # We are inheriting from CreateView. Therefore, every time that super().post is run, the form
        # that CreateView manages for us is automatically validated and submitted. This happens
        # regardless of what keys the post data dictionary contains. This is a problem because
        # if, for example, we make a POST request to delete a department, then, as a side effect, the create department 
        # form will be validated even though the user 
        # did not interact with it, and it will display an error (since the user would not have input anything into it). 
        # To fix this we need to dynamically change the function pointer of get_form_kwargs for all post types
        # that do not concern the creation form (e.g. edit, delete), so that we can stop the POST data being 
        # passed to the form and hence stop the form from trying to validate and submit. We can't statically override
        # get_form_kwargs in the current class because then we will always be removing the POST data from the form,
        # even when we want to actually use the form.

        old_get_form_kwargs = self.get_form_kwargs
        self.get_form_kwargs = self.custom_get_form_kwargs

        result = super().post(request, *args, **kwargs)

        self.get_form_kwargs = old_get_form_kwargs



        return result

    def get_template_names(self):
        return ["department_manager.html"]

    # def get_form_kwargs(self):
    #     _kwargs = super().get_form_kwargs()

    #     print("GOT KWARGS: THE DATA IS: ", _kwargs)

    #     _kwargs.pop("data", None)
    #     _kwargs.pop("files", None)

    #     print("GOT KWARGS: THE DATA AFTERRRRR IS: ", _kwargs)

    #     return _kwargs

    
    # def end(self, request):

    #     return render(request, "edit_user.html", {"id" : request.GET.get("id"),
    #                                               "user" : self.user,
    #                                               "form" : self.form,
    #                                               "error" : self.error})

    





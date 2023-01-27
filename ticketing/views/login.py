from ticketing.utility import auth_util
from ticketing.forms import LoginForm

from django.shortcuts import render

def login_view(request):

    if request.user.is_authenticated:
        return auth_util.landing_redirect_by_role(request.user.role)


    form = LoginForm()

    #badLoginStr = ""

   # if request.POST:
    #     email = (request.POST.get('email')).lower()
    #     password = request.POST.get('password')

    #     user = authenticate(email = email, password = password)
    #     if user is not None:
    #         if user.is_active:
    #             auth_login(request, user)
    #             if user.user_type == 'student':
    #                 return redirect('login_landing')
    #             elif user.user_type == 'administrator':
    #                 return redirect('admin_panel')
    #             elif user.user_type == 'director':
    #                 return redirect('director_panel')
    #             elif user.user_type == 'teacher':
    #                 return redirect('teacher_panel')
    #             return redirect('development')
    #     messages.add_message(request, messages.ERROR, "Incorrect email or password")
    # else:
    #     pass

    context = {"form" : form}
            #"badLoginStr" : badLoginStr}

    return render(request, "login.html", context)

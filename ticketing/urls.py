from django.urls import path, include
from django.contrib.auth import views
from .views import *
from .forms import LoginForm
from student_query_system import settings

urlpatterns = [
    path('', home.home, name='home'),
    # path('login/', login.LoginView.as_view(), name='login')
    path('login/', views.LoginView.as_view(
        template_name="login.html",
        authentication_form=LoginForm
    ),
    name = 'login'
    ),
    path('logout/', views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path('signup/', auth.SignupView.as_view(), name = 'signup')
]
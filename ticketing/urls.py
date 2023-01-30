from django.urls import path, include
from django.contrib.auth import views
from .views import *
from .forms import LoginForm
from student_query_system import settings

urlpatterns = [
    path('', home.home, name='home'),
    path('login/', auth.CustomLoginView.as_view(
            template_name="login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ),
        name = 'login'
    ),
    path('logout/', views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path('signup/', auth.SignupView.as_view(), name = 'signup'),
    path('specialist_dashboard/', specialist.DashboardView.as_view(), name = 'specialist_dashboard')
]
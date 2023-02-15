from django.urls import path, include
from django.contrib.auth import views
from .views import *
from .forms import LoginForm
from student_query_system import settings

urlpatterns = [
    path('', home.home, name='home'),
    path(
        'login/',
        auth.CustomLoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path(
        'logout/',
        views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name='logout',
    ),
    path('signup/', auth.SignupView.as_view(), name='signup'),
    path(
        'specialist_dashboard/',
        specialist_inbox.SpecialistInboxView.as_view(),
        name='specialist_dashboard',
    ),
    path(
        'specialist_claim_ticket/<int:pk>',
        specialist_claim_ticket.SpecialistClaimTicketView.as_view(),
        name='specialist_claim_ticket',
    ),
    path(
        'create_ticket/',
        student_ticket.StudentTicketView.as_view(),
        name='create_ticket',
    ),
    path(
        'student_dashboard/',
        student_inbox.StudentInboxView.as_view(),
        name='student_dashboard',
    ),
    path('ticket/', ticket_view.TicketView.as_view(), name='ticket'),
    path(
        'create_ticket/',
        student_ticket.StudentTicketView.as_view(),
        name='create_ticket',
    ),
    path(
        'ticket/<int:pk>/',
        student_message.StudentMessageView.as_view(),
        name='student_message',
    ),
    path(
        'view_ticket/<int:pk>',
        specialist_message.SpecialistMessageView.as_view(),
        name='specialist_message',
    ),
]

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from ticketing.decorators import *
from django.contrib.auth.decorators import login_required
class DashboardView(View):
    @method_decorator(roles_allowed(allowed_roles = ['SP', 'DI']), login_required)

    def get(self, request, *args, **kwargs):
        return render(request, 'specialist_db.html')

    
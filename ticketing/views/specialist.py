from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ticketing import mixins

class DashboardView(LoginRequiredMixin, mixins.RoleRequiredMixin, View):
    raise_exception = True
    required_roles = ['SP', 'DI']
    def get(self, request, *args, **kwargs):
        return render(request, 'specialist_db.html')
    # def test_func(self):
    #     return self.request.user.role in ['SP', 'DI']
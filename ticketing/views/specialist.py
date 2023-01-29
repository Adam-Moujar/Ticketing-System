from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = True
    def get(self, request, *args, **kwargs):
        return render(request, 'specialist_db.html')
    def test_func(self):
        return self.request.user.role == 'SP'
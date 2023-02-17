from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []

    def test_func(self):
        if None in self.required_roles:
            return True
        elif self.request.user.is_anonymous:
            return False

        return self.request.user.role in self.required_roles

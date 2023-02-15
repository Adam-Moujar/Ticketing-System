from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []

    def test_func(self):
        return self.request.user.role in self.required_roles


# class AuthorisedUserMixin(UserPassesTestMixin):
#     allowed_ids = []

#     def test_func(self):
#         return self.request.user.id in self.allowed_ids

from .const import user_roles

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, blank=False)

    role = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        return super(User, self).save(*args, **kwargs)
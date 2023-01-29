from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from .const import role as Role

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        if not first_name:
            raise ValueError("Enter a first name")
        if not last_name:
            raise ValueError("Enter a last name")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.role = 2
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.role = 3
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True, blank = False)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    ROLE_CHOICES = (
        (Role.STUDENT, 'Student'),
        (Role.SPECIALIST, 'Specialist'),
        (Role.DIRECTOR, 'Director'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=Role.SPECIALIST)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)


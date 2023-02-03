from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

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
        user.role = 'ST'
        user.save(using=self._db)
        return user

    def create_specialist(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        if not first_name:
            raise ValueError("Enter a first name")
        if not last_name:
            raise ValueError("Enter a last name")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.role = 'SP'
        user.save(using=self._db)
        return user
    
    def create_director(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")
        if not first_name:
            raise ValueError("Enter a first name")
        if not last_name:
            raise ValueError("Enter a last name")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.role = 'DI'
        user.save(using=self._db)
        return user
    
        
    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'DI'
        user.save(using=self._db)
        return user

# seed done
class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True, blank = False)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    class Role(models.TextChoices):
        STUDENT = 'ST'
        SPECIALIST = 'SP'
        DIRECTOR = 'DI'

    role = models.CharField(
        max_length = 2,
        choices = Role.choices,
        default = Role.STUDENT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

# seed done
class Department(models.Model):
    name = models.CharField(max_length = 100, blank = False, unique = True)

# seed done 
class SpecialistDepartment(models.Model):
    specialist = models.ForeignKey('User', on_delete= models.CASCADE, db_column ='specialist')
    department = models.ForeignKey('Department', on_delete= models.CASCADE, db_column ='department')

# seed done 
class SpecialistInbox(models.Model):
    specialist = models.ForeignKey('User', on_delete= models.CASCADE, db_column = 'specialist')
    ticket = models.ForeignKey('Ticket', on_delete= models.CASCADE, db_column = 'ticket')

# seed done 
class Ticket(models.Model):
    student = models.ForeignKey('User', on_delete= models.CASCADE)
    department = models.ForeignKey('Department', on_delete = models.CASCADE)
    header = models.CharField(max_length = 100, blank = False)
    ## status: for open closed archived bla bla bla 

# seed done 
class Message(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete = models.CASCADE)
    content = models.TextField(blank = False)
    date_time = models.DateTimeField(auto_now_add=True)

class StudentMessage(Message):
    pass

class SpecialistMessage(Message):
    responder = models.ForeignKey('User', on_delete= models.CASCADE, db_column = 'responder')

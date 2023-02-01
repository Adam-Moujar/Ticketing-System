from datetime import date, timedelta, datetime
import django
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ticketing.models import User
import random

from django.db.models import Q
#   TODO
#   should have two admins
#   need to figure out how to assign roles.

class Command(BaseCommand):
    PASSWORD = "Hello123%"

    COUNT = 15

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        User.objects.all().delete()

        self.create_test_users()

    def create_test_users(self):
        first_name = "Luke"
        last_name = "Test"

        User.objects.create_user("luke@7ic.net", self.PASSWORD, "Luke", "Test")

        for i in range(self.COUNT):
            User.objects.create_user("luke" + str(i + 1) + "@7ic.net", 
                                        self.PASSWORD, 
                                        "Luke" + str(i + 1), 
                                        "Test" + str(i + 1))


from django.core.management.base import BaseCommand, CommandError
from ticketing.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Department.objects.all().delete()

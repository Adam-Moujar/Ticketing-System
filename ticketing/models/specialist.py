from django.db import models
from django.utils.translation import gettext_lazy as _


class SpecialistDepartment(models.Model):
    specialist = models.ForeignKey(
        'User', on_delete=models.CASCADE, db_column='specialist'
    )
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, db_column='department'
    )


class SpecialistInbox(models.Model):
    specialist = models.ForeignKey(
        'User', on_delete=models.CASCADE, db_column='specialist'
    )
    ticket = models.ForeignKey(
        'Ticket', on_delete=models.CASCADE, db_column='ticket'
    )

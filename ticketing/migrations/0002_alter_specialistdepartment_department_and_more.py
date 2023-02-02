# Generated by Django 4.1.5 on 2023-02-01 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialistdepartment',
            name='department',
            field=models.ForeignKey(db_column='department', on_delete=django.db.models.deletion.CASCADE, to='ticketing.department'),
        ),
        migrations.AlterField(
            model_name='specialistdepartment',
            name='specialist',
            field=models.ForeignKey(db_column='specialist', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='specialistinbox',
            name='specialist',
            field=models.ForeignKey(db_column='specialist', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='specialistinbox',
            name='ticket',
            field=models.ForeignKey(db_column='ticket', on_delete=django.db.models.deletion.CASCADE, to='ticketing.ticket'),
        ),
    ]

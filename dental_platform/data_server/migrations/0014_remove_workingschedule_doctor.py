# Generated by Django 5.1.1 on 2024-09-21 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_server', '0013_remove_doctorschedule_day_doctorschedule_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workingschedule',
            name='doctor',
        ),
    ]

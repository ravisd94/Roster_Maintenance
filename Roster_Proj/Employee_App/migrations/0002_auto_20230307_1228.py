# Generated by Django 3.2.16 on 2023-03-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_master',
            name='Break_End_Time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance_master',
            name='Break_Start_Time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-16 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0005_auto_20211113_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('MANAGER', 'Manager'), ('ENGINEER', 'Engineer'), ('NEW_HIRE', 'New Hire')], default='SUPERUSER', max_length=15),
        ),
    ]

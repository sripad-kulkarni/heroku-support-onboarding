from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import ROLES
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    firstlogin = models.BooleanField(default=True)
    role = models.CharField(max_length=15, choices=ROLES, default = 'SUPERUSER')
    startdate = models.DateField(max_length=True, default=datetime.datetime.now)
    enddate = models.DateField(max_length=True, default=datetime.datetime.now)

    def __str__(self):
        return self.user.username

class weeks_data(models.Model):
    weekid = models.IntegerField()
    weektitle = models.CharField(max_length=200)

class content(models.Model):
    weeks_data = models.ForeignKey(weeks_data, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    task = models.TextField()

class targets(models.Model):
    target_id = models.IntegerField()
    target = models.CharField(max_length=150)

class non_dev_weeks_data(models.Model):
    weekid = models.IntegerField()
    weektitle = models.CharField(max_length=200)

class non_dev_content(models.Model):
    weeks_data = models.ForeignKey(non_dev_weeks_data, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    task = models.TextField()

class non_dev_targets(models.Model):
    target_id = models.IntegerField()
    target = models.CharField(max_length=150)

class onboarding(models.Model):
    newhire = models.CharField(max_length=50, primary_key=True)
    trailguide = models.CharField(max_length=50)
    onboardingbuddy = models.CharField(max_length=50)
    the_manager = models.CharField(max_length=50)
    progress = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)

class newhire_weeks(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    weekid = models.IntegerField()
    weektitle = models.CharField(max_length=200)
    status = models.FloatField(default='0.0')

class newhire_content(models.Model):
    newhire_weeks = models.ForeignKey(newhire_weeks, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    task = models.TextField()
    status = models.BooleanField(default=False)

class newhire_targets(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    target_id = models.IntegerField()
    target = models.CharField(max_length=150)
    status = models.BooleanField(default=False)




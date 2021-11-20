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

class onboarding(models.Model):
    newhire = models.CharField(max_length=50, primary_key=True)
    trailguide = models.CharField(max_length=50)
    onboardingbuddy = models.CharField(max_length=50)

class weeks_data(models.Model):
    weekid = models.IntegerField(primary_key=True)
    weektitle = models.CharField(max_length=200, null=True)

class week_content(models.Model):
    weeks_data = models.ForeignKey(weeks_data, on_delete=models.CASCADE)
    content = models.TextField(null=True)

    def __str__(self):
        return self.weeks_data.weekid
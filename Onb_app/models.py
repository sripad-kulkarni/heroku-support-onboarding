from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import ROLES

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    firstlogin = models.BooleanField(default=True)
    role = models.CharField(max_length=15, choices=ROLES, default = 'SUPERUSER')

    def __str__(self):
        return self.user.username

class onboarding(models.Model):
    trailguide = models.CharField(max_length=50)
    onboardingbuddy = models.CharField(max_length=50)
    newhire = models.CharField(max_length=50)
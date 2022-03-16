from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import ROLES, ACCESS_STATUS
import datetime
from django.core.validators import RegexValidator

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
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 16, default='')

    def __str__(self):
        return self.user.username

class access_section(models.Model):
    s_id = models.IntegerField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class access_item(models.Model):
    access_section = models.ForeignKey(access_section, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class weeks_data(models.Model):
    weekid = models.IntegerField()
    weektitle = models.CharField(max_length=200)

class content(models.Model):
    weeks_data = models.ForeignKey(weeks_data, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class targets(models.Model):
    target_id = models.IntegerField()
    target = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class onboarding(models.Model):
    newhire = models.CharField(max_length=50, primary_key=True)
    trailguide = models.CharField(max_length=50)
    onboardingbuddy = models.CharField(max_length=50)
    the_manager = models.CharField(max_length=50)
    progress = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class newhire_access_section(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    s_id = models.IntegerField()
    name = models.CharField(max_length=50)
    status = models.FloatField(default='0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class newhire_access_item(models.Model):
    newhire_access_section = models.ForeignKey(newhire_access_section, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    name = models.TextField()
    status = models.CharField(max_length=15, default = 'Not Requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class newhire_weeks(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    weekid = models.IntegerField()
    weektitle = models.CharField(max_length=200)
    status = models.FloatField(default='0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class newhire_content(models.Model):
    newhire_weeks = models.ForeignKey(newhire_weeks, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    task = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class newhire_targets(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    target_id = models.IntegerField()
    target = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class audit_logger(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    action = models.CharField(max_length=250)

class resources(models.Model):
    onboarding = models.ForeignKey(onboarding, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    
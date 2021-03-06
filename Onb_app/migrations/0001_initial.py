# Generated by Django 3.2.9 on 2021-12-15 18:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='onboarding',
            fields=[
                ('newhire', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('trailguide', models.CharField(max_length=50)),
                ('onboardingbuddy', models.CharField(max_length=50)),
                ('the_manager', models.CharField(max_length=50)),
                ('progress', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='targets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.IntegerField()),
                ('target', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='weeks_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekid', models.IntegerField()),
                ('weektitle', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('firstlogin', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('MANAGER', 'Manager'), ('ENGINEER', 'Engineer'), ('NEW_HIRE', 'New Hire')], default='SUPERUSER', max_length=15)),
                ('startdate', models.DateField(default=datetime.datetime.now, max_length=True)),
                ('enddate', models.DateField(default=datetime.datetime.now, max_length=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='newhire_weeks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekid', models.IntegerField()),
                ('weektitle', models.CharField(max_length=200)),
                ('status', models.FloatField(default='0.0')),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding')),
            ],
        ),
        migrations.CreateModel(
            name='newhire_targets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.IntegerField()),
                ('target', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=False)),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding')),
            ],
        ),
        migrations.CreateModel(
            name='newhire_content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('task', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('newhire_weeks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.newhire_weeks')),
            ],
        ),
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('task', models.TextField()),
                ('weeks_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.weeks_data')),
            ],
        ),
    ]

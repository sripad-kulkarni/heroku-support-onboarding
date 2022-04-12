# Generated by Django 3.2.9 on 2022-03-30 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0013_rename_active_onboarding_finished'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onboarding',
            name='finished',
        ),
        migrations.CreateModel(
            name='onb_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding')),
            ],
        ),
    ]
# Generated by Django 3.2.9 on 2022-03-30 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0015_alter_onb_status_onboarding'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboarding',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='onb_status',
        ),
    ]

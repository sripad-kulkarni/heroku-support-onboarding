# Generated by Django 3.2.9 on 2022-03-30 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0012_auto_20220325_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onboarding',
            old_name='active',
            new_name='finished',
        ),
    ]

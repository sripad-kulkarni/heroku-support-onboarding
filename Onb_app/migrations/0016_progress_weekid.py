# Generated by Django 3.2.9 on 2021-11-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0015_progress_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='weekid',
            field=models.IntegerField(null=True),
        ),
    ]

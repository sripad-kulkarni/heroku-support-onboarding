# Generated by Django 3.2.9 on 2022-03-30 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0014_auto_20220330_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onb_status',
            name='onboarding',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding'),
        ),
    ]

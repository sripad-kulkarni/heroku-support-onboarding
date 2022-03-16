# Generated by Django 3.2.9 on 2022-03-16 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0008_auto_20220313_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=500)),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding')),
            ],
        ),
    ]

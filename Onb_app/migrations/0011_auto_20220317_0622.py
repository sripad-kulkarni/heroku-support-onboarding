# Generated by Django 3.2.9 on 2022-03-17 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0010_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_item',
            name='name',
            field=models.TextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='content',
            name='task',
            field=models.TextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='newhire_access_item',
            name='name',
            field=models.TextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='newhire_content',
            name='task',
            field=models.TextField(max_length=50000),
        ),
    ]
# Generated by Django 3.2.9 on 2022-03-11 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0005_newhire_access_item_newhire_access_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='access_item',
            name='access_section',
        ),
        migrations.RemoveField(
            model_name='content',
            name='weeks_data',
        ),
        migrations.RemoveField(
            model_name='newhire_access_item',
            name='newhire_access_section',
        ),
        migrations.RemoveField(
            model_name='newhire_access_section',
            name='onboarding',
        ),
        migrations.RemoveField(
            model_name='newhire_content',
            name='newhire_weeks',
        ),
        migrations.RemoveField(
            model_name='newhire_targets',
            name='onboarding',
        ),
        migrations.RemoveField(
            model_name='newhire_weeks',
            name='onboarding',
        ),
        migrations.DeleteModel(
            name='targets',
        ),
        migrations.DeleteModel(
            name='access_item',
        ),
        migrations.DeleteModel(
            name='access_section',
        ),
        migrations.DeleteModel(
            name='content',
        ),
        migrations.DeleteModel(
            name='newhire_access_item',
        ),
        migrations.DeleteModel(
            name='newhire_access_section',
        ),
        migrations.DeleteModel(
            name='newhire_content',
        ),
        migrations.DeleteModel(
            name='newhire_targets',
        ),
        migrations.DeleteModel(
            name='newhire_weeks',
        ),
        migrations.DeleteModel(
            name='onboarding',
        ),
        migrations.DeleteModel(
            name='weeks_data',
        ),
    ]

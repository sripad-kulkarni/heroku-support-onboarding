# Generated by Django 3.2.9 on 2022-03-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0007_access_item_access_section_audit_logger_content_newhire_access_item_newhire_access_section_newhire_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit_logger',
            name='action',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='newhire_access_item',
            name='status',
            field=models.CharField(default='Not Requested', max_length=15),
        ),
    ]
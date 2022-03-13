# Generated by Django 3.2.9 on 2022-03-11 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onb_app', '0006_auto_20220311_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='access_section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='audit_logger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=50)),
                ('action', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='onboarding',
            fields=[
                ('newhire', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('trailguide', models.CharField(max_length=50)),
                ('onboardingbuddy', models.CharField(max_length=50)),
                ('the_manager', models.CharField(max_length=50)),
                ('progress', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='targets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.IntegerField()),
                ('target', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
            name='newhire_weeks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekid', models.IntegerField()),
                ('weektitle', models.CharField(max_length=200)),
                ('status', models.FloatField(default='0.0')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('newhire_weeks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.newhire_weeks')),
            ],
        ),
        migrations.CreateModel(
            name='newhire_access_section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('status', models.FloatField(default='0.0')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.onboarding')),
            ],
        ),
        migrations.CreateModel(
            name='newhire_access_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('name', models.TextField()),
                ('status', models.CharField(default='NOT YET REQUESTED', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('newhire_access_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.newhire_access_section')),
            ],
        ),
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('task', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('weeks_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.weeks_data')),
            ],
        ),
        migrations.CreateModel(
            name='access_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('access_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Onb_app.access_section')),
            ],
        ),
    ]

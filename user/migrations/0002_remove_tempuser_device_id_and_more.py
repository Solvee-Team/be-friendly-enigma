# Generated by Django 4.0.6 on 2022-07-29 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempuser',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='tempuser',
            name='group_number',
        ),
        migrations.RemoveField(
            model_name='tempuser',
            name='insurance_carrier',
        ),
        migrations.RemoveField(
            model_name='tempuser',
            name='is_test_user',
        ),
        migrations.RemoveField(
            model_name='tempuser',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='tempuser',
            name='os',
        ),
    ]

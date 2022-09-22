# Generated by Django 4.0.6 on 2022-09-15 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_style',
            field=models.CharField(blank=True, choices=[('orange', 'orange'), ('purple', 'purple'), ('aquamarine', 'aquamarine'), ('aqua', 'aqua'), ('beige', 'beige'), ('yellow', 'yellow'), ('green', 'green'), ('blue', 'blue')], default='purple', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(blank=True, choices=[('orange', 'orange'), ('purple', 'purple'), ('aquamarine', 'aquamarine'), ('aqua', 'aqua'), ('beige', 'beige'), ('yellow', 'yellow'), ('green', 'green'), ('blue', 'blue')], default='light', max_length=100, null=True),
        ),
    ]
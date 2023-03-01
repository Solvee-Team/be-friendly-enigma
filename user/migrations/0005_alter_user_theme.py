# Generated by Django 4.0.6 on 2022-09-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_chat_style_user_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='theme',
            field=models.CharField(blank=True, choices=[('black', 'black'), ('light', 'light'), ('dark', 'dark')], default='light', max_length=100, null=True),
        ),
    ]

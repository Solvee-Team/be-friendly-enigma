# Generated by Django 3.2.6 on 2022-08-17 09:15

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.TextField(blank=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Dialog',
                'verbose_name_plural': 'Dialogs',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('is_read', models.BooleanField(default=False, verbose_name='Is Read')),
                ('dialog', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.dialog')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('-created',),
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]

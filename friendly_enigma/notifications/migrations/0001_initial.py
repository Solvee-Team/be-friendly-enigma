# Generated by Django 4.0.6 on 2022-07-15 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(db_index=True, default=False)),
                ('actor_object_id', models.CharField(max_length=255)),
                ('verb', models.CharField(choices=[('assign', 'assign'), ('complete', 'complete'), ('due', 'due'), ('create', 'create'), ('have', 'have')], max_length=50)),
                ('text', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('is_sent', models.BooleanField(db_index=True, default=False)),
                ('type', models.CharField(choices=[('Custom', 'Custom'), ('Assessment', 'Assessment'), ('Goal', 'Goal'), ('Message', 'Message'), ('Exercise_Plan', 'Exercise_Plan'), ('Appointment', 'Appointment'), ('Manager_Assign', 'Manager_Assign'), ('Member_Assign', 'Member_Assign')], default='Custom', max_length=50)),
                ('data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('actor_content_type', models.ForeignKey(limit_choices_to=models.Q(('app_label', 'chat'), ('model', 'message')), on_delete=django.db.models.deletion.CASCADE, related_name='notify_actor', to='contenttypes.contenttype')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp',),
                'index_together': {('recipient', 'is_read')},
            },
        ),
    ]

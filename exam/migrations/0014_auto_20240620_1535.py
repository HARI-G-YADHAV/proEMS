# Generated by Django 3.2.12 on 2024-06-20 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0013_auto_20240617_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dutyallotment',
            name='teacher_id',
        ),
        migrations.AddField(
            model_name='dutyallotment',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.16 on 2025-04-08 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals_app', '0002_alter_proposal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='evaluator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_proposals', to=settings.AUTH_USER_MODEL),
        ),
    ]

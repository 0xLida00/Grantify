# Generated by Django 4.2.16 on 2025-04-05 11:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support_app', '0004_faq_status_faq_thumbs_down_faq_thumbs_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='voted_down',
            field=models.ManyToManyField(blank=True, related_name='voted_down_faqs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='faq',
            name='voted_up',
            field=models.ManyToManyField(blank=True, related_name='voted_up_faqs', to=settings.AUTH_USER_MODEL),
        ),
    ]

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from accounts_app.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_notification_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationPreference = apps.get_model('alerts_app', 'NotificationPreference')
        if not hasattr(instance, 'notification_preferences'):
            NotificationPreference.objects.create(user=instance)
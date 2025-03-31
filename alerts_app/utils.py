from django.core.mail import send_mail
from alerts_app.models import Notification

def send_email_notification(user, subject, message):
    '''Sends an email notification to the user if email notifications are enabled.'''
    if user.notification_preferences.email_enabled:
        send_mail(
            subject,
            message,
            'noreply@sample.ie',
            [user.email],
            fail_silently=False,
        )

def create_in_app_notification(user, message):
    '''Creates an in-app notification for the user if in-app notifications are enabled.'''
    if user.notification_preferences.in_app_enabled:
        Notification.objects.create(
            user=user,
            notification_type='in_app',
            message=message,
        )
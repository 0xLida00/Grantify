from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from alerts_app.models import Notification, NotificationPreference

User = get_user_model()

class AlertsAppTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a test notification
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type="in_app",
            message="Test notification message",
            is_read=False,
        )

        # The NotificationPreference is now automatically created by the signal
        self.notification_preference = self.user.notification_preferences

    # Test: List Notifications
    def test_notification_list(self):
        response = self.client.get(reverse('notification_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alerts_app/notification_list.html')
        self.assertContains(response, self.notification.message)

    # Test: Mark Notification as Read
    def test_mark_notification_as_read(self):
        response = self.client.post(reverse('mark_notification_as_read', args=[self.notification.pk]))
        self.assertEqual(response.status_code, 302)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    # Test: Notification Preferences - GET
    def test_notification_preferences_get(self):
        response = self.client.get(reverse('notification_preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alerts_app/notification_preferences.html')
        self.assertContains(response, 'Notification Preferences')

    # Test: Notification Preferences - POST
    def test_notification_preferences_post(self):
        response = self.client.post(reverse('notification_preferences'), {
            'email_enabled': False,
            'sms_enabled': True,
            'in_app_enabled': False,
            'push_enabled': True,
        })
        self.assertEqual(response.status_code, 302)
        self.notification_preference.refresh_from_db()
        self.assertFalse(self.notification_preference.email_enabled)
        self.assertTrue(self.notification_preference.sms_enabled)
        self.assertFalse(self.notification_preference.in_app_enabled)
        self.assertTrue(self.notification_preference.push_enabled)

    # Test: Create Notification
    def test_create_notification(self):
        notification = Notification.objects.create(
            user=self.user,
            notification_type="email",
            message="New test notification",
            is_read=False,
        )
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(notification.message, "New test notification")

    # Test: Delete Notification
    def test_delete_notification(self):
        notification_id = self.notification.id
        self.notification.delete()
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())
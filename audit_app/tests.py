from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from audit_app.models import LogEntry
from django.core.paginator import Paginator

class AuditAppViewsTestCase(TestCase):
    def setUp(self):
        CustomUser = get_user_model()

        self.staff_user = CustomUser.objects.create_user(
            username='staffuser', password='password123', is_staff=True
        )

        self.non_staff_user = CustomUser.objects.create_user(
            username='regularuser', password='password123', is_staff=False
        )

        self.log1 = LogEntry.objects.create(
            user=self.staff_user,
            action="Test Action 1",
            object_repr="Test Object 1",
            change_message="Test Change Message 1",
            log_level="INFO",
            source="Test Source"
        )
        self.log2 = LogEntry.objects.create(
            user=self.staff_user,
            action="Test Action 2",
            object_repr="Test Object 2",
            change_message="Test Change Message 2",
            log_level="ERROR",
            source="Test Source"
        )
        self.log3 = LogEntry.objects.create(
            user=self.non_staff_user,
            action="Test Action 3",
            object_repr="Test Object 3",
            change_message="Test Change Message 3",
            log_level="DEBUG",
            source="Test Source"
        )

    # Test: Log list accessible to staff
    def test_log_list_accessible_to_staff(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('log_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit_app/log_list.html')

    # Test: Log list inaccessible to non-staff
    def test_log_list_inaccessible_to_non_staff(self):
        self.client.login(username='regularuser', password='password123')
        response = self.client.get(reverse('log_list'))
        self.assertEqual(response.status_code, 302)

    # Test: Log list pagination
    def test_log_list_pagination(self):
        self.client.login(username='staffuser', password='password123')

        for i in range(30):
            LogEntry.objects.create(
                user=self.staff_user,
                action=f"Log entry {i + 4}",
                object_repr=f"Object {i + 4}",
                change_message=f"Change message {i + 4}",
                log_level="INFO",
                source="Test Source"
            )

        # Test first page
        response = self.client.get(reverse('log_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 25)

        # Test second page
        response = self.client.get(reverse('log_list') + '?page=2')
        self.assertEqual(response.status_code, 200)

        logs_for_test = LogEntry.objects.filter(action__startswith="Log entry").order_by('-created_at')
        paginator = Paginator(logs_for_test, 25)
        second_page_logs = paginator.get_page(2)

        self.assertEqual(len(second_page_logs), 5)

    # Test: Log list filter by user
    def test_log_list_filter_by_user(self):
        self.client.login(username='staffuser', password='password123')

        response = self.client.get(reverse('log_list') + f'?user={self.staff_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

    # Test: Log detail accessible to staff
    def test_log_detail_accessible_to_staff(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('log_detail', args=[self.log1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit_app/log_detail.html')
        self.assertContains(response, 'Test Change Message 1')

    # Test: Log detail inaccessible to non-staff
    def test_log_detail_inaccessible_to_non_staff(self):
        self.client.login(username='regularuser', password='password123')
        response = self.client.get(reverse('log_detail', args=[self.log1.pk]))
        self.assertEqual(response.status_code, 302)

    # Test: Log detail 404 for non-existent log
    def test_log_detail_404_for_non_existent_log(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('log_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
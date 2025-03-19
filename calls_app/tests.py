from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import GrantCall, GrantQuestion

class CallsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = get_user_model().objects.create_user(
            username="staffuser",
            email="staffuser@example.com",
            password="TestPassword123",
            is_staff=True
        )
        self.non_staff_user = get_user_model().objects.create_user(
            username="regularuser",
            email="regularuser@example.com",
            password="TestPassword123",
            is_staff=False
        )
        self.grant_call = GrantCall.objects.create(
            title="Test Grant Call",
            description="This is a test grant call.",
            deadline="2025-12-31",
            eligibility="Must be a registered organization.",
            budget=10000.00,
            status="open",
            created_by=self.staff_user
        )
        self.create_url = reverse("grant_call_create")
        self.list_url = reverse("grant_call_list")
        self.detail_url = reverse("grant_call_detail", kwargs={"pk": self.grant_call.pk})
        self.update_url = reverse("grant_call_update", kwargs={"pk": self.grant_call.pk})
        self.delete_url = reverse("grant_call_delete", kwargs={"pk": self.grant_call.pk})

    # 1. Test grant call list view
    def test_grant_call_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calls_app/grant_call_list.html")
        self.assertContains(response, self.grant_call.title)

    # 2. Test grant call detail view
    def test_grant_call_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calls_app/grant_call_detail.html")
        self.assertContains(response, self.grant_call.title)
        self.assertContains(response, self.grant_call.description)

    # 3. Test grant call create view (staff user)
    def test_grant_call_create_view_staff_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        data = {
            "title": "New Grant Call",
            "description": "Description for new grant call.",
            "deadline": "2025-12-31",
            "eligibility": "Eligibility criteria.",
            "budget": 5000.00,
            "status": "open",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(GrantCall.objects.filter(title="New Grant Call").exists())

    # 4. Test grant call create view (non-staff user)
    def test_grant_call_create_view_non_staff_user(self):
        self.client.login(username="regularuser", password="TestPassword123")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-staff users

    # 5. Test grant call update view (staff user)
    def test_grant_call_update_view_staff_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        data = {
            "title": "Updated Grant Call",
            "description": "Updated description.",
            "deadline": "2025-12-31",
            "eligibility": "Updated eligibility criteria.",
            "budget": 15000.00,
            "status": "closed",
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.grant_call.refresh_from_db()
        self.assertEqual(self.grant_call.title, "Updated Grant Call")
        self.assertEqual(self.grant_call.status, "closed")

    # 6. Test grant call update view (non-staff user)
    def test_grant_call_update_view_non_staff_user(self):
        self.client.login(username="regularuser", password="TestPassword123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-staff users

    # 7. Test grant call delete view (staff user)
    def test_grant_call_delete_view_staff_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(GrantCall.objects.filter(pk=self.grant_call.pk).exists())

    # 8. Test grant call delete view (non-staff user)
    def test_grant_call_delete_view_non_staff_user(self):
        self.client.login(username="regularuser", password="TestPassword123")
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-staff users

    # 9. Test adding questions to a grant call
    def test_add_questions_to_grant_call(self):
        self.client.login(username="staffuser", password="TestPassword123")
        data = {
            "title": "New Grant Call",
            "description": "Description for new grant call.",
            "deadline": "2025-12-31",
            "eligibility": "Eligibility criteria.",
            "budget": 5000.00,
            "status": "open",
            "questions-TOTAL_FORMS": "1",
            "questions-INITIAL_FORMS": "0",
            "questions-MIN_NUM_FORMS": "0",
            "questions-MAX_NUM_FORMS": "1000",
            "questions-0-question_text": "What is your organization's mission?",
            "questions-0-question_type": "open",
        }
        response = self.client.post(self.create_url, data)
        print("Response content:", response.content.decode())  # Debugging: Print response content
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(GrantCall.objects.filter(title="New Grant Call").exists())
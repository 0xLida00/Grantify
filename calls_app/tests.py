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
            is_staff=True,
            role="admin"
        )
        self.org_user = get_user_model().objects.create_user(
            username="orguser",
            email="orguser@example.com",
            password="TestPassword123",
            role="org"
        )
        self.applicant_user = get_user_model().objects.create_user(
            username="applicantuser",
            email="applicantuser@example.com",
            password="TestPassword123",
            role="applicant"
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
        self.apply_url = reverse("apply_grant_call", kwargs={"pk": self.grant_call.pk})

    # Test grant call list view
    def test_grant_call_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calls_app/grant_call_list.html")
        self.assertContains(response, self.grant_call.title)

    # Test grant call detail view
    def test_grant_call_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calls_app/grant_call_detail.html")
        self.assertContains(response, self.grant_call.title)
        self.assertContains(response, self.grant_call.description)

    # Test grant call create view (admin user)
    def test_grant_call_create_view_admin_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        data = {
            "title": "New Grant Call",
            "description": "Description for new grant call.",
            "deadline": "2025-12-31",  # Ensure the date is in YYYY-MM-DD format
            "eligibility": "Eligibility criteria.",
            "budget": 5000.00,
            "status": "open",
            "questions-TOTAL_FORMS": "1",  # Required for formset
            "questions-INITIAL_FORMS": "0",  # Required for formset
            "questions-MIN_NUM_FORMS": "0",
            "questions-MAX_NUM_FORMS": "1000",
            "questions-0-question_text": "What is your organization's mission?",
            "questions-0-question_type": "open",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(GrantCall.objects.filter(title="New Grant Call").exists())

    # Test grant call create view (non-admin user)
    def test_grant_call_create_view_non_admin_user(self):
        self.client.login(username="applicantuser", password="TestPassword123")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-admin users

    # Test grant call update view (admin user)
    def test_grant_call_update_view_admin_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        data = {
            "title": "Updated Grant Call",
            "description": "Updated description.",
            "deadline": "2025-12-31",  # Ensure the date is in YYYY-MM-DD format
            "eligibility": "Updated eligibility criteria.",
            "budget": 15000.00,
            "status": "closed",
            "questions-TOTAL_FORMS": "1",  # Required for formset
            "questions-INITIAL_FORMS": "0",  # Required for formset
            "questions-MIN_NUM_FORMS": "0",
            "questions-MAX_NUM_FORMS": "1000",
            "questions-0-question_text": "What is your organization's updated mission?",
            "questions-0-question_type": "open",
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.grant_call.refresh_from_db()
        self.assertEqual(self.grant_call.title, "Updated Grant Call")
        self.assertEqual(self.grant_call.status, "closed")

    # Test grant call update view (non-admin user)
    def test_grant_call_update_view_non_admin_user(self):
        self.client.login(username="applicantuser", password="TestPassword123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-admin users

    # Test grant call delete confirmation page (admin user)
    def test_grant_call_delete_confirmation_page_admin_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calls_app/grant_call_confirm_delete.html")
        self.assertContains(response, "Are you sure you want to delete this grant call?")

    # Test grant call delete view (admin user)
    def test_grant_call_delete_view_admin_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(GrantCall.objects.filter(pk=self.grant_call.pk).exists())

    # Test grant call delete view (non-admin user)
    def test_grant_call_delete_view_non_admin_user(self):
        self.client.login(username="applicantuser", password="TestPassword123")
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-admin users

    # Test applying to a grant call (applicant user)
    def test_apply_grant_call_applicant_user(self):
        self.client.login(username="applicantuser", password="TestPassword123")
        response = self.client.post(self.apply_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful application
        self.assertRedirects(response, self.list_url)

    # Test applying to a grant call (non-applicant user)
    def test_apply_grant_call_non_applicant_user(self):
        self.client.login(username="staffuser", password="TestPassword123")
        response = self.client.post(self.apply_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-applicant users
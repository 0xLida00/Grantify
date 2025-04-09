from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now, timedelta
from proposals_app.models import Proposal
from evaluation_app.models import Evaluation
from .models import Report
from django.db import models

User = get_user_model()

class ReportsAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", is_staff=True)
        self.client.login(username="testuser", password="password123")

        self.report_data = {
            'total_proposals': 10,
            'proposals_by_status': [
                {'status': 'submitted', 'count': 5},
                {'status': 'draft', 'count': 3},
                {'status': 'accepted', 'count': 2},
            ],
            'average_score': 4.5,
            'recent_proposals': 7,
        }
        self.report = Report.objects.create(
            generated_by=self.user,
            report_data=self.report_data,
        )

        # Create proposals and evaluations
        Proposal.objects.create(title="Proposal 1", status="submitted", applicant=self.user)
        Proposal.objects.create(title="Proposal 2", status="draft", applicant=self.user)
        Evaluation.objects.create(score=4.5)

    def test_report_string_representation(self):
        self.assertEqual(str(self.report), f"Report generated on {self.report.generated_at}")

    # Test the generate_report view
    def test_generate_report(self):
        response = self.client.post(reverse('generate_report'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(Report.objects.count(), 2)

    def test_generate_report_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('generate_report'))
        self.assertEqual(response.status_code, 403)

    # Test the report_list view
    def test_report_list(self):
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reports")
        self.assertEqual(len(response.context['page_obj']), 1)

    # Test the report_detail view
    def test_report_detail(self):
        response = self.client.get(reverse('report_detail', args=[self.report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Report Details")
        self.assertContains(response, "total_proposals")
        self.assertContains(response, "recent_proposals")
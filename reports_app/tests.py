from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from reports_app.models import Report
from proposals_app.models import Proposal, GrantCall
from evaluation_app.models import Evaluation
from django.utils.timezone import now, timedelta

User = get_user_model()

class ReportsAppTests(TestCase):
    def setUp(self):
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username='staffuser', password='password123', is_staff=True
        )

        # Create a non-staff user
        self.non_staff_user = User.objects.create_user(
            username='regularuser', password='password123', is_staff=False
        )

        # Create a GrantCall instance with a valid deadline
        self.grant_call = GrantCall.objects.create(
            title="Grant Call 1",
            description="Test Grant Call",
            deadline=now().date() + timedelta(days=30),
            eligibility="Eligibility criteria",
            budget=100000.00,
            created_by=self.staff_user
        )

        # Create sample proposals
        self.proposal1 = Proposal.objects.create(
            title="Proposal 1", status="accepted", applicant=self.staff_user, grant_call=self.grant_call
        )
        self.proposal2 = Proposal.objects.create(
            title="Proposal 2", status="rejected", applicant=self.staff_user, grant_call=self.grant_call
        )

        # Create sample evaluations
        self.evaluation1 = Evaluation.objects.create(
            proposal=self.proposal1, score=85, evaluator=self.staff_user
        )
        self.evaluation2 = Evaluation.objects.create(
            proposal=self.proposal2, score=90, evaluator=self.staff_user
        )

        # Create sample reports
        self.report1 = Report.objects.create(
            generated_by=self.staff_user,
            report_data={"key": "value"},
            generated_at=now()
        )
        self.report2 = Report.objects.create(
            generated_by=self.staff_user,
            report_data={"key": "value"},
            generated_at=now() - timedelta(days=1)
        )

    def test_dashboard_access_control(self):
        # Non-staff user should be redirected to the admin login page
        self.client.login(username='regularuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

        # Staff user should have access
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_statistics(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "2")  # Total proposals
        self.assertContains(response, "2")  # Total evaluations
        self.assertContains(response, "87.5")  # Average score
        self.assertContains(response, "1")  # Accepted proposals
        self.assertContains(response, "1")  # Rejected proposals

    def test_report_list_access_control(self):
        # Non-staff user should be redirected to the admin login page
        self.client.login(username='regularuser', password='password123')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

        # Staff user should have access
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)

    def test_report_list_pagination(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('report_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.report1.generated_by.username)
        self.assertContains(response, self.report1.generated_at.strftime('%Y-%m-%d'))

    def test_report_detail_access_control(self):
        # Non-staff user should be redirected to the admin login page
        self.client.login(username='regularuser', password='password123')
        response = self.client.get(reverse('report_detail', args=[self.report1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

        # Staff user should have access
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('report_detail', args=[self.report1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_report_detail_correct_display(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('report_detail', args=[self.report1.pk]))
        self.assertContains(response, self.report1.report_data)
        self.assertContains(response, self.report1.generated_by.username)

    def test_report_detail_non_existent(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('report_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
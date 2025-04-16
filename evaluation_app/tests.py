from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from evaluation_app.models import Evaluation
from proposals_app.models import Proposal, GrantCall
from alerts_app.models import NotificationPreference
from datetime import datetime, timedelta

User = get_user_model()

class EvaluationAppTests(TestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.evaluator = User.objects.create_user(username='evaluator', password='password')
        self.applicant = User.objects.create_user(username='applicant', password='password')

        # Create notification preferences for users
        NotificationPreference.objects.create(user=self.admin)
        NotificationPreference.objects.create(user=self.evaluator)
        NotificationPreference.objects.create(user=self.applicant)

        # Create a grant call
        self.grant_call = GrantCall.objects.create(
            title="Test Grant Call",
            description="Test Description",
            status="open",
            budget=10000,
            deadline=datetime.now() + timedelta(days=30),
            created_by=self.admin
        )

        # Create a proposal
        self.proposal = Proposal.objects.create(
            title="Test Proposal",
            applicant=self.applicant,
            grant_call=self.grant_call,
            status="submitted"
        )

        # Create an evaluation
        self.evaluation = Evaluation.objects.create(
            proposal=self.proposal,
            evaluator=self.evaluator,
            status="pending"
        )

    def test_assign_evaluator(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('assign_evaluators'), {
            'proposal': self.proposal.id,
            'evaluator': self.evaluator.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Evaluation.objects.filter(proposal=self.proposal, evaluator=self.evaluator).exists())

    def test_monitor_evaluations(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('monitor_evaluations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Proposal")
        self.assertContains(response, self.evaluator.username)

    def test_evaluator_dashboard(self):
        self.client.login(username='evaluator', password='password')
        response = self.client.get(reverse('evaluator_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Proposal")

    def test_submit_evaluation(self):
        self.client.login(username='evaluator', password='password')
        response = self.client.post(reverse('submit_evaluation', args=[self.evaluation.id]), {
            'score': 8.5,
            'feedback': 'Good proposal.'
        })
        self.assertEqual(response.status_code, 302)
        self.evaluation.refresh_from_db()
        self.assertEqual(self.evaluation.score, 8.5)
        self.assertEqual(self.evaluation.feedback, 'Good proposal.')
        self.assertEqual(self.evaluation.status, 'completed')

    def test_submit_evaluation_invalid_score(self):
        self.client.login(username='evaluator', password='password')
        response = self.client.post(reverse('submit_evaluation', args=[self.evaluation.id]), {
            'score': 15,
            'feedback': 'Invalid score test.'
        })
        self.assertEqual(response.status_code, 200)
        self.evaluation.refresh_from_db()
        self.assertNotEqual(self.evaluation.score, 15)
        self.assertEqual(self.evaluation.status, 'pending')

    def test_feedback_detail(self):
        self.evaluation.score = 9.0
        self.evaluation.feedback = "Excellent proposal."
        self.evaluation.status = "completed"
        self.evaluation.save()

        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('feedback_detail', args=[self.evaluation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Excellent proposal.")
        self.assertContains(response, "Test Proposal")
        self.assertContains(response, "9.0")
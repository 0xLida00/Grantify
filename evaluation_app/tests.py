from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from evaluation_app.models import Evaluation
from proposals_app.models import Proposal, GrantCall
from alerts_app.models import Notification
from django.utils.timezone import now

User = get_user_model()

class EvaluationAppTestCase(TestCase):
    def setUp(self):
        # Create a staff user (admin)
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_staff=True
        )

        # Create an evaluator
        self.evaluator = User.objects.create_user(
            username='evaluator',
            password='evaluatorpassword',
            is_staff=False
        )

        # Create a grant call
        self.grant_call = GrantCall.objects.create(
            title="Test Grant Call",
            description="Test Description",
            deadline=now().date(),
            eligibility="Eligibility Criteria",
            budget=100000.00,
            created_by=self.admin_user
        )

        # Create a proposal
        self.proposal = Proposal.objects.create(
            title="Test Proposal",
            status="submitted",
            applicant=self.evaluator,
            grant_call=self.grant_call
        )

        # Create an evaluation
        self.evaluation = Evaluation.objects.create(
            proposal=self.proposal,
            evaluator=self.evaluator,
            score=None,
            feedback=None,
            status="pending"
        )

    # Test: Assign evaluators
    def test_assign_evaluators(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('assign_evaluators'), {
            'proposal': self.proposal.id,
            'evaluator': self.evaluator.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Evaluation.objects.filter(proposal=self.proposal, evaluator=self.evaluator).exists())

    # Test: Monitor evaluations
    def test_monitor_evaluations(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('monitor_evaluations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluation_app/monitor_evaluations.html')
        self.assertContains(response, self.proposal.title)

    # Test: Evaluator dashboard
    def test_evaluator_dashboard(self):
        self.client.login(username='evaluator', password='evaluatorpassword')
        response = self.client.get(reverse('evaluator_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluation_app/evaluator_dashboard.html')
        self.assertContains(response, self.proposal.title)

    # Test: Submit evaluation
    def test_submit_evaluation(self):
        self.client.login(username='evaluator', password='evaluatorpassword')
        response = self.client.post(reverse('submit_evaluation', args=[self.evaluation.id]), {
            'score': 8.5,
            'feedback': "Great proposal!",
        })
        self.assertEqual(response.status_code, 302)
        self.evaluation.refresh_from_db()
        self.assertEqual(self.evaluation.status, 'completed')
        self.assertEqual(self.evaluation.score, 8.5)
        self.assertEqual(self.evaluation.feedback, "Great proposal!")

    # Test: Feedback detail (admin only)
    def test_feedback_detail(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('feedback_detail', args=[self.evaluation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluation_app/feedback_detail.html')
        self.assertContains(response, self.proposal.title)

    # Test: Unauthorized access to feedback detail
    def test_feedback_detail_unauthorized(self):
        self.client.login(username='evaluator', password='evaluatorpassword')
        response = self.client.get(reverse('feedback_detail', args=[self.evaluation.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)
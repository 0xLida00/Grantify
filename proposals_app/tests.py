from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from calls_app.models import GrantResponse
from .models import Proposal, GrantCall
from datetime import datetime, timedelta

User = get_user_model()

class ProposalsAppTests(TestCase):
    def setUp(self):
        self.applicant = User.objects.create_user(username='applicant', password='password', role='applicant')
        self.staff_user = User.objects.create_user(username='adminuser', password='password', is_staff=True, role='admin')
        self.evaluator = User.objects.create_user(username='evaluator', password='password', role='evaluator')

        self.grant_call = GrantCall.objects.create(
            title="Test Grant Call",
            description="Test Description",
            status="open",
            budget=10000,
            deadline=datetime.now() + timedelta(days=30),
            created_by=self.staff_user
        )

        self.proposal1 = Proposal.objects.create(
            title="Proposal 1",
            applicant=self.applicant,
            grant_call=self.grant_call,
            status="draft"
        )
        self.proposal2 = Proposal.objects.create(
            title="Proposal 2",
            applicant=self.applicant,
            grant_call=self.grant_call,
            status="submitted"
        )

        self.response = GrantResponse.objects.create(
            question=self.grant_call.questions.create(question_text="Test Question", question_type="open"),
            user=self.applicant,
            grant_call=self.grant_call,
            response="Test Response"
        )

    # Test Proposal List View
    def test_proposal_list_view_authenticated(self):
        self.client.login(username='applicant', password='password')
        response = self.client.get(reverse('proposals_app:proposal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proposal 1")
        self.assertContains(response, "Proposal 2")

    def test_proposal_list_view_unauthenticated(self):
        response = self.client.get(reverse('proposals_app:proposal_list'))
        self.assertEqual(response.status_code, 302)

    # Test Admin Proposal List View
    def test_admin_proposal_list_view_staff(self):
        self.client.login(username='adminuser', password='password')
        response = self.client.get(reverse('proposals_app:admin_proposal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proposal 1")
        self.assertContains(response, "Proposal 2")

    def test_admin_proposal_list_view_non_staff(self):
        self.client.login(username='applicant', password='password')
        response = self.client.get(reverse('proposals_app:admin_proposal_list'))
        self.assertEqual(response.status_code, 302)

    # Test Proposal Detail View
    def test_proposal_detail_view(self):
        self.client.login(username='applicant', password='password')
        response = self.client.get(reverse('proposals_app:proposal_detail', args=[self.proposal1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proposal 1")
        self.assertContains(response, "Test Description")
        self.assertContains(response, "Test Question")
        self.assertContains(response, "Test Response")
        if self.response.file:
            self.assertContains(response, "Download File")

    def test_proposal_detail_view_non_owner(self):
        self.client.login(username='evaluator', password='password')
        response = self.client.get(reverse('proposals_app:proposal_detail', args=[self.proposal1.pk]))
        self.assertEqual(response.status_code, 403)

    # Test Proposal Update View
    def test_proposal_update_view(self):
        self.client.login(username='applicant', password='password')

        response = self.client.post(reverse('proposals_app:proposal_update', args=[self.proposal1.pk]), {
            'question_1_response': 'Updated Answer',
        })

        self.assertEqual(response.status_code, 302)

        self.proposal1.refresh_from_db()

        self.assertEqual(self.proposal1.title, 'Proposal 1')
        self.assertEqual(self.proposal1.description, '')

        updated_response = GrantResponse.objects.get(
            question=self.grant_call.questions.first(),
            user=self.applicant,
            grant_call=self.grant_call
        )
        self.assertEqual(updated_response.response, 'Updated Answer')

    # Test Proposal Delete View
    def test_proposal_delete_view(self):
        self.client.login(username='applicant', password='password')
        response = self.client.post(reverse('proposals_app:proposal_delete', args=[self.proposal1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Proposal.objects.filter(pk=self.proposal1.pk).exists())

    # Test Evaluator Assignment in Admin Proposal List View
    def test_admin_assign_evaluator(self):
        self.client.login(username='adminuser', password='password')
        response = self.client.post(reverse('proposals_app:admin_proposal_list'), {
            'proposal_id': self.proposal1.pk,
            'evaluator_id': self.evaluator.pk
        })
        self.assertEqual(response.status_code, 302)
        self.proposal1.refresh_from_db()
        self.assertEqual(self.proposal1.evaluator, self.evaluator)
        self.assertEqual(self.proposal1.status, 'under_review')
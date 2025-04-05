from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import SupportTicket, Feedback, FAQ
from .forms import SupportTicketForm, FeedbackForm

User = get_user_model()

# Model Tests:
class SupportTicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject="Test Subject",
            description="Test Description",
            priority="high",
        )

    # Ticket_creation: Tests the creation of a SupportTicket.
    def test_1_ticket_creation(self):
        self.assertEqual(self.ticket.subject, "Test Subject")
        self.assertEqual(self.ticket.description, "Test Description")
        self.assertEqual(self.ticket.priority, "high")
        self.assertEqual(self.ticket.status, "open")
        self.assertEqual(str(self.ticket), f"Ticket: {self.ticket.subject} ({self.ticket.status})")


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.feedback = Feedback.objects.create(
            user=self.user,
            message="Great service!",
            rating=5,
        )

    # Feedback_creation: Tests the creation of a Feedback.
    def test_2_feedback_creation(self):
        self.assertEqual(self.feedback.message, "Great service!")
        self.assertEqual(self.feedback.rating, 5)
        self.assertEqual(str(self.feedback), f"Feedback from {self.user.username} (Rating: {self.feedback.rating})")


class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is the purpose of this app?",
            answer="This app helps manage support tickets and FAQs.",
        )

    # Faq_creation: Tests the creation of an FAQ.
    def test_3_faq_creation(self):
        self.assertEqual(self.faq.question, "What is the purpose of this app?")
        self.assertEqual(self.faq.answer, "This app helps manage support tickets and FAQs.")
        self.assertEqual(str(self.faq), self.faq.question)

# Form Tests:
class SupportTicketFormTest(TestCase):
    # Valid_form: Tests a valid SupportTicketForm.
    def test_4_valid_form(self):
        form_data = {
            "subject": "Test Subject",
            "description": "Test Description",
            "priority": "medium",
        }
        form = SupportTicketForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Invalid_form: Tests an invalid SupportTicketForm.
    def test_5_invalid_form(self):
        form_data = {
            "subject": "",  # Missing subject
            "description": "Test Description",
            "priority": "medium",
        }
        form = SupportTicketForm(data=form_data)
        self.assertFalse(form.is_valid())


class FeedbackFormTest(TestCase):
    # Valid_form: Tests a valid FeedbackForm.
    def test_6_valid_form(self):
        form_data = {
            "message": "Great service!",
            "rating": 4,
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Invalid_form: Tests an invalid FeedbackForm.
    def test_7_invalid_form(self):
        form_data = {
            "message": "",
            "rating": 4,
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())


# API Tests:
class SupportTicketAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    # Create_support_ticket: Tests creating a support ticket as an authenticated user.
    def test_8_create_support_ticket(self):
        data = {
            "subject": "Test Subject",
            "description": "Test Description",
            "priority": "high",
        }
        response = self.client.post("/api/support-tickets/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SupportTicket.objects.count(), 1)
        self.assertEqual(SupportTicket.objects.first().subject, "Test Subject")

    # Create_support_ticket_unauthenticated: Tests creating a support ticket as an unauthenticated user.
    def test_9_create_support_ticket_unauthenticated(self):
        self.client.logout()
        data = {
            "subject": "Test Subject",
            "description": "Test Description",
            "priority": "high",
        }
        response = self.client.post("/api/support-tickets/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FeedbackAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    # Create_feedback: Tests creating feedback as an authenticated user.
    def test_10_create_feedback(self):
        data = {
            "message": "Great service!",
            "rating": 5,
        }
        response = self.client.post("/api/feedback/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.first().message, "Great service!")

    # Create_feedback_unauthenticated: Tests creating feedback as an unauthenticated user.
    def test_11_create_feedback_unauthenticated(self):
        self.client.logout()
        data = {
            "message": "Great service!",
            "rating": 5,
        }
        response = self.client.post("/api/feedback/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FAQAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        FAQ.objects.create(
            question="What is the purpose of this app?",
            answer="This app helps manage support tickets and FAQs.",
            status="published",
        )

    # Fetch_faqs: Tests fetching FAQs.
    def test_12_fetch_faqs(self):
        response = self.client.get("/api/faqs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["question"], "What is the purpose of this app?")

# FAQ Tests:
class AdminFAQViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username="staffuser", password="password123", is_staff=True)
        self.regular_user = User.objects.create_user(username="regularuser", password="password123")
        self.faq = FAQ.objects.create(
            question="What is the purpose of this app?",
            answer="This app helps manage support tickets and FAQs.",
            status="published",
        )

    # Test: Admin can view FAQ list
    def test_admin_can_view_faq_list(self):
        self.client.login(username="staffuser", password="password123")
        response = self.client.get("/admin-panel/faqs/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.faq.question)

    # Test: Regular user cannot view FAQ list
    def test_regular_user_cannot_view_faq_list(self):
        self.client.login(username="regularuser", password="password123")
        response = self.client.get("/admin-panel/faqs/")
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, "/admin/login/?next=/admin-panel/faqs/")

    # Test: Admin can create FAQ
    def test_admin_can_create_faq(self):
        self.client.login(username="staffuser", password="password123")
        data = {
            "question": "How do I reset my password?",
            "answer": "Go to the settings page and click 'Reset Password'.",
            "status": "published",
        }
        response = self.client.post("/admin-panel/faqs/create/", data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FAQ.objects.count(), 2)
        self.assertTrue(FAQ.objects.filter(question="How do I reset my password?").exists())

    # Test: Admin can edit FAQ
    def test_admin_can_edit_faq(self):
        self.client.login(username="staffuser", password="password123")
        data = {
            "question": "Updated Question",
            "answer": "Updated Answer",
            "status": "draft",
        }
        response = self.client.post(f"/admin-panel/faqs/{self.faq.id}/edit/", data)
        self.assertEqual(response.status_code, 302)
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.question, "Updated Question")
        self.assertEqual(self.faq.status, "draft")

    # Test: Admin can delete FAQ
    def test_admin_can_delete_faq(self):
        self.client.login(username="staffuser", password="password123")
        response = self.client.post(f"/admin-panel/faqs/{self.faq.id}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FAQ.objects.count(), 0)

# FAQ Voting Tests:
class FAQVotingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.faq = FAQ.objects.create(
            question="What is the purpose of this app?",
            answer="This app helps manage support tickets and FAQs.",
            status="published",
        )

    # Test: User can vote thumbs up
    def test_user_can_vote_thumbs_up(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/faqs/{self.faq.id}/vote/", {"vote_type": "up"})
        self.assertEqual(response.status_code, 200)
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.thumbs_up, 1)
        self.assertEqual(self.faq.thumbs_down, 0)

    # Test: User can vote thumbs down
    def test_user_can_vote_thumbs_down(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/faqs/{self.faq.id}/vote/", {"vote_type": "down"})
        self.assertEqual(response.status_code, 200)
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.thumbs_up, 0)
        self.assertEqual(self.faq.thumbs_down, 1)

    # Test: User can switch votes
    def test_user_can_switch_votes(self):
        self.client.login(username="testuser", password="password123")
        self.client.post(f"/faqs/{self.faq.id}/vote/", {"vote_type": "up"})
        self.client.post(f"/faqs/{self.faq.id}/vote/", {"vote_type": "down"})
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.thumbs_up, 0)
        self.assertEqual(self.faq.thumbs_down, 1)
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser

class AccountsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile', kwargs={'username': 'testuser'})
        self.password_change_url = reverse('password_change')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123',
            role='applicant'
        )

    # Test GET request for signup page
    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/signup.html')

    # Test POST request for valid signup
    def test_signup_post_valid(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123',
            'role': 'applicant',
        }
        response = self.client.post(self.signup_url, data)
        user_model = get_user_model()
        self.assertTrue(user_model.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('home'))

    # Test POST request for invalid signup (password mismatch)
    def test_signup_post_invalid(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPassword123',
            'password2': 'WrongPassword123',
            'role': 'applicant',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='newuser').exists())

    # Test GET request for login page
    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/login.html')

    # Test POST request for valid login
    def test_login_post_valid(self):
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('home'))

    # Test POST request for invalid login
    def test_login_post_invalid(self):
        data = {
            'username': 'testuser',
            'password': 'WrongPassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password!")

    # Test logout functionality
    def test_logout(self):
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('home'))

    # Test profile page access for logged-in user
    def test_profile_access(self):
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/profile.html')

    # Test unauthorized access to another user's profile
    def test_profile_unauthorized_access(self):
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='OtherPassword123'
        )
        self.client.login(username='testuser', password='TestPassword123')
        
        response = self.client.get(reverse('profile', kwargs={'username': 'otheruser'}))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
    
    # Test password change functionality
    def test_password_change(self):
        self.client.login(username='testuser', password='TestPassword123')
        data = {
            'old_password': 'TestPassword123',
            'new_password1': 'NewPassword123',
            'new_password2': 'NewPassword123',
        }
        response = self.client.post(self.password_change_url, data)
        self.assertRedirects(response, reverse('profile', kwargs={'username': 'testuser'}))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123'))
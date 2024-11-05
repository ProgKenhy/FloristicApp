from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from users.forms import UserLoginForm, UserRegistrationForm

from users.models import EmailVerification, User


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'John',
            'username': 'John_user', 'email': 'test@gmail.com',
            'password1': 'buratinoCA21', 'password2': 'buratinoCA21',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(days=2)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create_user(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context['form'].errors)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.login_url = reverse('users:login')

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_successful(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

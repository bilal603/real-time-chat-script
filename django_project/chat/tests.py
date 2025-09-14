
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message  # If you have a Message model

class SignupLoginLogoutTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.signup_url = reverse('signup')
		self.chat_url = reverse('chat')
		self.logout_url = reverse('logout')
		self.user_data = {
			'name': 'Bilal',
			'last_name': 'Cakir',
			'email': 'bilal@example.com'
		}

	def test_signup(self):
		response = self.client.post(self.signup_url, self.user_data)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(email='bilal@example.com').exists())

	def test_login_existing_user(self):
		User.objects.create_user(username='bilal@example.com', email='bilal@example.com', first_name='Bilal', last_name='Cakir')
		response = self.client.post(self.signup_url, self.user_data)
		self.assertEqual(response.status_code, 302)

	def test_logout(self):
		user = User.objects.create_user(username='bilal@example.com', email='bilal@example.com', first_name='Bilal', last_name='Cakir')
		self.client.force_login(user)
		response = self.client.get(self.logout_url)
		self.assertEqual(response.status_code, 302)

# Integration test for chat message (if Message model exists)
class ChatMessageTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='test@example.com', email='test@example.com', first_name='Test', last_name='User')
		self.client.force_login(self.user)
		self.chat_url = reverse('chat')

	def test_chat_page_access(self):
		response = self.client.get(self.chat_url)
		self.assertEqual(response.status_code, 200)

	# Add more tests for message sending, typing indicator, etc. as needed

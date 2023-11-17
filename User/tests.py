# https://testdriven.io/blog/django-custom-user-model/

# from django.contrib.auth import get_user_model
# from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import MyAuthor, VC_Codes
from .serializers import ForgotPasswordSerializer


class ForgotPasswordViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_forgot_password_valid_email(self):
        user = MyAuthor.objects.create(email='newuser@gmail.com', name='Test User')
        url = reverse('forgot-password') 
        data = {'email': 'newuser@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertIn('to_email' in response.data, True)

    def test_forgot_password_invalid_email(self):
        url = reverse('forgot-password')
        data = {'email': 'invalid_email'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_user_not_found(self):
        url = reverse('forgot-password')
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
# https://testdriven.io/blog/django-custom-user-model/

# from django.contrib.auth import get_user_model
# from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from User.models import MyAuthor,VC_Codes
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


'''Implement LoginViewTest'''
class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('login')
    
    def athenticate(self, email, passw, name, role):
        # SignUp
        response = self.client.post(
            reverse("signup"),
            {
                "name": name,
                "email": email,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify Email
        response = self.client.post(
            reverse("verify-email"),
            {
                "name": name,
                "password": passw,
                "role": role,
                "email": email,
                "code": VC_Codes.objects.get(email=email).vc_code,
            }
        )      
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Login
        response = self.client.post(
            reverse("login"),
            {
                "email": email,
                "password": passw,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get Token
        token = response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
    def test_login_checkAuthentication(self):
        self.athenticate("test_email@gmail.com", "test_pass", "test_name", "customer")       
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_login_method_notAllowed(self):
        self.athenticate("test_email@gmail.com", "test_pass", "test_name", "customer")
        response = self.client.delete(self.url, {
                                                    "password": "test_pass",
                                                        "email": "test_email@gmail.com"
                                                    })
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)




# https://testdriven.io/blog/django-custom-user-model/

# from django.contrib.auth import get_user_model
# from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import MyAuthor, VC_Codes
from .serializers import ForgotPasswordSerializer
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
from User.views import OrderViewSet2
from User.models import MyAuthor
from rest_framework_simplejwt.tokens import AccessToken


# class UsersManagersTests(TestCase):

#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="normal@user.com", password="foo")
#         self.assertEqual(user.email, "normal@user.com")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(TypeError):
#             User.objects.create_user()
#         with self.assertRaises(TypeError):
#             User.objects.create_user(email="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="", password="foo")

#     def test_create_superuser(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
#         self.assertEqual(admin_user.email, "super@user.com")
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(admin_user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 email="super@user.com", password="foo", is_superuser=False)


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

    def test_forgot_password_successful_email_sent(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            url = reverse('forgot-password')  
            data = {'email': 'test@example.com'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            # self.assertIn('to_email' in response.data, True)

    def test_forgot_password_invalid_method(self):
        url = reverse('forgot-password') 
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_forgot_password_code_generation(self):
        user = MyAuthor.objects.create(email='n.haghighy@gmail.com', name='Test User')
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            url = reverse('forgot-password')  
            data = {'email': 'n.haghighy@gmail.com'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            vc_code = VC_Codes.objects.get(email='n.haghighy@gmail.com').vc_code
            self.assertTrue(vc_code.isalnum() and len(vc_code) == 10)

    def test_forgot_password_code_update_on_resend(self):
        user = MyAuthor.objects.create(email='n.haghighy@gmail.com', name='Test User')
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            url = reverse('forgot-password') 
            data = {'email': 'n.haghighy@gmail.com'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            initial_vc_code = VC_Codes.objects.get(email='n.haghighy@gmail.com').vc_code
            response_resend = self.client.post(url, data, format='json')
            self.assertEqual(response_resend.status_code, status.HTTP_201_CREATED)
            updated_vc_code = VC_Codes.objects.get(email='n.haghighy@gmail.com').vc_code
            self.assertNotEqual(initial_vc_code, updated_vc_code)


# class OrderViewSet2Test(APITestCase):
#     # def setUp(self):
#     #     self.user = MyAuthor.objects.create(
#     #         email='test@gmail.com',
#     #         name='test',
#     #         is_staff=False,
#     #         is_active=True,
#     #         is_superuser=False,
#     #         is_admin=False,
#     #         password='1234',
#     #         role='customer'
#     #     )
#     #     access_token = Token.objects.create(user=self.user)
#     #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token.key)
    
#     def test_get_order(self):
#         self.user = MyAuthor.objects.create(
#             email='test@gmail.com',
#             password='1234',
#         )
#         access_token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token.key)
#         response = self.client.get(reverse('order'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderViewSet2TestCase(APITestCase):
    def setUp(self):
        self.url = reverse('order')
    
    def athenticate(self):
        # self.client.post(
        #     reverse("signup"),
        #     {
        #         "email": "jonathan@app.com",
        #         "password": "password##!123",
        #         "name": "jonathan",
        #     },
        # )

        response = self.client.post(
            reverse("login"),
            {
                "email": "admin@gmail.com",
                "password": "1234",
            },
        )
        print(response.data)
        token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
    def test_order_list(self):
        self.athenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

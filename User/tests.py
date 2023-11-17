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
from rest_framework import status
from User.views import OrderViewSet2
from User.models import MyAuthor
from .models import *
from .serializers import *
import random , string
from django.db import connection

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


class ForgotPassVerifyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_forgot_pass_verify_successful(self):
        user = MyAuthor.objects.create(email='test2@gmail.com', name='Test User')
        vc_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        VC_Codes.objects.create(email=user.email, name=user.name, vc_code=vc_code)
        url = reverse('fp-verify')  
        data = {'email': 'test2@gmail.com', 'code': vc_code}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_pass_verify_invalid_email(self):
        url = reverse('fp-verify')
        data = {'email': 'invalid_email', 'code': '1234567890'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_pass_verify_user_not_found(self):
        url = reverse('fp-verify')
        data = {'email': 'nonexistent@example.com', 'code': '1234567890'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forgot_pass_verify_wrong_code(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        VC_Codes.objects.create(email=user.email, name=user.name, vc_code='1234567890')
        url = reverse('fp-verify')  
        data = {'email': 'test@example.com', 'code': '0987654321'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('verification code is wrong', response.data)

    def test_forgot_pass_verify_invalid_data(self):
        url = reverse('fp-verify')  
        data = {'email': 'test@example.com'}  # Missing 'code' field
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_pass_verify_code_deleted_after_successful_verification(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        vc_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        VC_Codes.objects.create(email=user.email, name=user.name, vc_code=vc_code)
        url = reverse('fp-verify') 
        data = {'email': 'test@example.com', 'code': vc_code}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(VC_Codes.DoesNotExist):
            VC_Codes.objects.get(email='test@example.com')

    def test_forgot_pass_verify_multiple_attempts(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        vc_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        VC_Codes.objects.create(email=user.email, name=user.name, vc_code=vc_code)
        url = reverse('fp-verify')
        for _ in range(3):
            data = {'email': 'test@example.com', 'code': 'wrong_code'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('verification code is wrong', response.data)
        data = {'email': 'test@example.com', 'code': vc_code}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ForgotPassSetNewPassTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_forgot_pass_set_new_pass_successful(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        url = reverse('fp-newpassword')  
        data = {'email': 'test@example.com', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpassword'))

    def test_forgot_pass_set_new_pass_invalid_email(self):
        url = reverse('fp-newpassword')  
        data = {'email': 'invalid_email', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_pass_set_new_pass_user_not_found(self):
        url = reverse('fp-newpassword')  
        data = {'email': 'nonexistent@example.com', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forgot_pass_set_new_pass_invalid_data(self):
        url = reverse('fp-newpassword')  
        data = {'email': 'test@example.com'}  # Missing 'password' field
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_pass_set_new_pass_password_update(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        old_password = user.password
        url = reverse('fp-newpassword') 
        data = {'email': 'test@example.com', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertNotEqual(user.password, old_password)

    def test_forgot_pass_set_new_pass_empty_password(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        url = reverse('fp-newpassword') 
        data = {'email': 'test@example.com', 'password': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_pass_set_new_pass_whitespace_password(self):
        user = MyAuthor.objects.create(email='test@example.com', name='Test User')
        url = reverse('fp-newpassword') 
        data = {'email': 'test@example.com', 'password': '    '}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DatabaseConnectionTests(TestCase):
    def test_database_connection_is_open(self):
        # Check if the database connection is open
        self.assertTrue(connection.connection is not None)

    def test_database_connection(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
        self.assertEqual(result, (1,))

    def test_database_name(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT current_database()')
            result = cursor.fetchone()
        self.assertEqual(result[0], 'test_nowaste')

    def test_create_and_retrieve_model(self):
        MyAuthor.objects.create(name='Test Item', email='test@example.com')
        # Retrieve the instance from the database
        test_item = MyAuthor.objects.get(name='Test Item')
        self.assertEqual(test_item.name, 'Test Item')
        self.assertEqual(test_item.email, 'test@example.com')

    def test_update_model(self):
        test_item = MyAuthor.objects.create(name='Test Item', email='test@example.com')
        test_item.name = 'Updated name'
        test_item.save()
        updated_item = MyAuthor.objects.get(email='test@example.com')
        self.assertEqual(updated_item.name, 'Updated name')

    def test_delete_model(self):
        MyAuthor.objects.create(name='Test Item', email='test@example.com')
        MyAuthor.objects.filter(name='Test Item').delete()
        deleted_item = MyAuthor.objects.filter(name='Test Item').first()
        self.assertIsNone(deleted_item)
        with self.assertRaises(MyAuthor.DoesNotExist):
            MyAuthor.objects.get(name='Test Item')

class OrderViewSet2TestCase(APITestCase):
    def setUp(self):
        self.url = reverse('order')
    
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
        
    def test_order_list(self):
        self.athenticate("test_email@gmail.com", "test_pass", "test_name", "customer")       
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_order_unathenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_order_method_notAllowed(self):
        self.athenticate("test_email@gmail.com", "test_pass", "test_name", "customer")
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        

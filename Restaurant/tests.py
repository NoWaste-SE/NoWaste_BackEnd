# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase, APIRequestFactory
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from User.views import OrderViewSet2
# from User.models import MyAuthor
# from rest_framework_simplejwt.tokens import AccessToken


# # creat test for orderviewset2
# class OrderViewSet2Test(APITestCase):
#     def setUp(self):
#         self.user = MyAuthor.objects.create(
#             email='test@gmail.com',
#             name='test',
#             is_staff=False,
#             is_active=True,
#             is_superuser=False,
#             is_admin=False,
#             password='1234',
#             role='customer'
#         )
#         access_token = AccessToken.for_user(self.user)
#         self.token = str(access_token)
#         self.factory = APIRequestFactory()
#         self.view = OrderViewSet2.as_view({'get': 'list'})
    
#     def test_order_list(self):
#         request = self.factory.get('/orders/')
#         request.headers = {'Authorization': 'Bearer ' + self.token}
#         response = self.view(request)
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        




        
from django.test import TestCase, Client
from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase, APIRequestFactory
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from User.views import OrderViewSet2
from User.models import *
# from rest_framework_simplejwt.tokens import AccessToken
from .models import *


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

class FoodModelTest(TestCase):
    def setUp(self):
        manager = RestaurantManager.objects.create(
            email='manager@example.com',
            name='Test Manager',
            password='managerpassword',
            role='restaurant'
        )
        restaurant = Restaurant.objects.create(
            type='Iranian',
            address='Test Address',
            name='Test Restaurant',
            manager=manager
        )
        self.food = Food.objects.create(
            name='Test Food',
            price=10.99,
            ingredients='Ingredient 1, Ingredient 2',
            restaurant=restaurant,
            remainder=50
        )

    def test_food_model_str(self):
        self.assertEqual(str(self.food), 'Test Food')

    def test_save_method_default_food_pic(self):
        food = Food.objects.create(
            name='Food with Default Pic',
            price=15.99,
            ingredients='Ingredient 3, Ingredient 4',
            restaurant=self.food.restaurant,
            remainder=20
        )
        self.assertEqual(food.food_pic, default_food_pic)

    def test_save_method_default_food_pic2(self):
        food = Food.objects.create(
            name='Food with None Pic2',
            price=19.99,
            ingredients='Ingredient 5, Ingredient 6',
            restaurant=self.food.restaurant,
            remainder=30
        )
        self.assertIsNone(food.food_pic2)

    def test_save_method_no_default_food_pic(self):
        food = Food.objects.create(
            name='Food without Default Pic',
            price=25.99,
            ingredients='Ingredient 7, Ingredient 8',
            restaurant=self.food.restaurant,
            remainder=40,
            food_pic='custom_food_pic_value'
        )
        self.assertEqual(food.food_pic, 'custom_food_pic_value')

    def test_price_field(self):
        self.assertEqual(self.food.price, 10.99)

    def test_remainder_field(self):
        self.assertEqual(self.food.remainder, 50)

    def test_no_default_values(self):
        food = Food.objects.create(
            name='Custom Food',
            price=18.75,
            ingredients='Ingredient 13, Ingredient 14',
            restaurant=self.food.restaurant,
            remainder=25,
            food_pic='custom_food_pic',
            food_pic2='custom_food_pic2'
        )
        self.assertEqual(food.food_pic, 'custom_food_pic')
        self.assertEqual(food.food_pic2, 'custom_food_pic2')

    def test_empty_reminder(self):
        food = Food.objects.create(
            name='',
            ingredients='',
            restaurant=self.food.restaurant
        )
        self.assertEqual(food.remainder, 0) 


    def test_food_creation_with_long_name(self):
        long_name = 'A' * 256
        food_long_name = Food(
            name=long_name,
            price=10.00,
            ingredients='Ingredient 23, Ingredient 24',
            restaurant=self.food.restaurant,
            remainder=50
        )
        with self.assertRaises(Exception):
            food_long_name.save()

    def test_food_creation_with_long_ingredients(self):
        long_ingredients = 'A' * 2049
        food_long_ingredients = Food(
            name='Long Ingredients Food',
            price=12.00,
            ingredients=long_ingredients,
            restaurant=self.food.restaurant,
            remainder=60
        )
        with self.assertRaises(Exception):
            food_long_ingredients.save()

    def test_food_creation_with_large_price(self):
        large_price = 10**20
        food_large_price = Food(
            name='Large Price Food',
            price=large_price,
            ingredients='Ingredient 25, Ingredient 26',
            restaurant=self.food.restaurant,
            remainder=70
        )
        with self.assertRaises(Exception):
            food_large_price.save()

    def test_food_creation_with_large_remainder(self):
        large_remainder = 10**20
        food_large_remainder = Food(
            name='Large Remainder Food',
            price=15.00,
            ingredients='Ingredient 27, Ingredient 28',
            restaurant=self.food.restaurant,
            remainder=large_remainder
        )
        with self.assertRaises(Exception):
            food_large_remainder.save()
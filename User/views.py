
from django.contrib.auth import get_user_model,logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
# from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from .utils import Util
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
###############################################
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_jwt.settings import api_settings

from rest_framework import generics
from django.template.loader import render_to_string
from django.core.validators import EmailValidator
from django.forms import ValidationError
import random , string
import json
# import jwt
from cities_light.models import Country, City

class VerifyEmail(APIView):
    def get_serializer_class(self, request):
        if request.data['role'] == "customer":
            return CreateCustomerSerializer
        elif request.data['role'] == "restaurant":
            return CreateRestaurantSerializer
    
    def post(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            try:
                user = VC_Codes.objects.get(email=user_data['email'])
            except VC_Codes.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user_data['code'] == user.vc_code:
                VC_Codes.objects.filter(vc_code = user.vc_code).delete()                
                serializer.save()
                myauthor = MyAuthor.objects.get(email = user_data['email'])
                myauthor.role = user_data['role']
                myauthor.save()
                return Response(user_data, status=status.HTTP_201_CREATED)
        return Response("verification code is wrong", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = BaseCreateUserSerializer()
        return Response(serializer.data)
    
class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception= True):
            vc_code = random.randint(100000, 999999)
            instance = serializer.save()
            instance.vc_code = vc_code
            instance.save()
            signupData = serializer.data
        else:
            return Response("email is already exist", status=status.HTTP_400_BAD_REQUEST)
        email = signupData['email']
        name = signupData['name']
        template = render_to_string('email_template.html', {'name': name, 'code': vc_code})
        data = {'to_email': email, 'body': template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
        Util.send_email(data)
        return Response(signupData, status=status.HTTP_201_CREATED)
    def get(self,request):
        serializer = SignUpSerializer()
        return Response(serializer.data)
    
    
class LoginView(APIView):
    serializer_class = MyAuthorSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try :
            user = MyAuthor.objects.get(email = email)

        except Exception as error :
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        if user is not None and user.check_password(password):
            id = user.id
            token, _ = Token.objects.get_or_create(user_id = id)
            if user.role == "customer":
                c = Customer.objects.get (email = email)
                name = c.name
                WalletBalance = c.wallet_balance
                listOfFavorite = list(c.list_of_favorites_res.values_list('name', flat=True))
                result_fav = []
                for r in listOfFavorite:
                    res = Restaurant.objects.get(name = r)
                    result_fav.append({'address': res.address, 'name': res.name, 'restaurant_image': res.restaurant_image, 'discount': res.discount, 'number': res.number, 'rate': res.rate, 'date_of_establishment': res.date_of_establishment, 'description': res.description, 'id': res.id})
                # listOfFavorite = list(c.list_of_favorites_res)
                return Response({'token': token.key,'id' : user.id, 'wallet_balance':WalletBalance, 'role':user.role, 'list_of_favorites_res':result_fav, 'name':name})
            else:
                r = RestaurantManager.objects.get(email = email)
                return Response({'token': token.key,'id' : user.id, 'role':user.role, 'name':r.name})

        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        serializer = MyAuthorSerializer()
        return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({'message': 'User logged out successfully'})


class ForgotPasswordViewSet(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer()
        validate_email = EmailValidator()
        email = request.data.get('email')
        try:
            validate_email.__call__(email)
        except ValidationError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = MyAuthor.objects.get(email=email)
        except MyAuthor.DoesNotExist:
            return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
        newCode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        try :
            u , created = VC_Codes.objects.get_or_create(email = user.email , name = "None")
            u.vc_code = newCode
            u.save()
        except Exception as error:
            # handle the exception
            # print("An exception occurred:", error)
            # return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return HttpResponse(json.dumps({'error': error}), mimetype="application/json")
        template = render_to_string('forgotpass_template.html',
            {'name': u.name,
                'code': newCode})
        data = {'to_email':u.email,'body':template, 'subject': 'NoWaste forgot password'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request):
        serializer = ForgotPasswordSerializer()
        return Response(serializer.data)

class ForgotPassVerify(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        validate_email = EmailValidator()
        if serializer.is_valid():
            email =serializer.validated_data['email']
            try:
                validate_email.__call__(email)
            except ValidationError as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = VC_Codes.objects.get(email=email)
            except VC_Codes.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user.vc_code == serializer.validated_data['code']:
                new_serializer = MyAuthorSerializer()
                return Response(new_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("verification code is wrong", status=status.HTTP_400_BAD_REQUEST)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = EmailVerificationSerializer()
        return Response(serializer.data)

class ForgotPassSetNewPass(APIView):
    def post(self, request):
        serializer = MyAuthorSerializer(data=request.data)
        validate_email = EmailValidator()
        if serializer.is_valid(raise_exception=True):
            email =serializer.validated_data['email']
            try:
                validate_email.__call__(email)
            except ValidationError as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = MyAuthor.objects.get(email=email)
            except MyAuthor.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = MyAuthorSerializer()
        return Response(serializer.data)

class ChangePasswordView(generics.UpdateAPIView):
    queryset = MyAuthor.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        user = request.user
        if(user.id != self.kwargs['pk']):
            return Response({"message": "Unathorized!"},status=status.HTTP_401_UNAUTHORIZED)
        super().update(request, *args, **kwargs) 
        return Response({"message" :"Password changed successfully!"},status= status.HTTP_200_OK)


class UpdateRetrieveProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Customer.objects.filter(id=self.kwargs['id'])
    def get_serializer_class(self):
        if (self.request.method == 'GET'):
            return CustomerSerializer
        else :
            return UpdateUserSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):
        # return self.partial_update(request, *args, **kwargs)
        # self.update(request,*args,**kwargs)\
        instance = self.get_object()
        for key , value in request.data.items():
            print(key , value)
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self,request,id):
        if ( request.user.id != id ):
            return Response({"message": "Unathorized!"},status= status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileView(generics.RetrieveAPIView):  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    lookup_field = 'id'
    def get_queryset(self):
        return Customer.objects.filter(id=self.kwargs['id'])

    def get_serializer_context(self):
        return {'id': self.kwargs['id']}



class RateRestaurantView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RateRestaurantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            try:
                restaurant = Restaurant.objects.get(name=name)
            except Restaurant.DoesNotExist:
                return Response("There is not any restaurant with the given name" , status=status.HTTP_404_NOT_FOUND)
            restaurant.rate = round(((restaurant.rate) * restaurant.count_rates + serializer.validated_data['rate']) / (restaurant.count_rates + 1), 1)
            restaurant.count_rates += 1
            restaurant.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = RateRestaurantSerializer()
        return Response(serializer.data)


class AddRemoveFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddRemoveFavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            try:
                restaurant = Restaurant.objects.get(name=name)
            except Restaurant.DoesNotExist:
                return Response("There is not any restaurant with the given name" , status=status.HTTP_404_NOT_FOUND)
            email = serializer.validated_data['email']
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response("There is not any customer with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user.list_of_favorites_res.filter(pk=restaurant.pk).exists():
                user.list_of_favorites_res.remove(restaurant)
            else:
                user.list_of_favorites_res.add(restaurant)
            user.save()
            listOfFavorite = list(user.list_of_favorites_res.values_list('name', flat=True))
            result_fav = []
            for r in listOfFavorite:
                res = Restaurant.objects.get(name = r)
                result_fav.append({'address': res.address, 'name': res.name, 'restaurant_image': res.restaurant_image, 'discount': res.discount, 'number': res.number, 'rate': res.rate, 'date_of_establishment': res.date_of_establishment, 'description': res.description, 'id': res.id})
            return Response({'list_of_favorites_res':result_fav}, status=status.HTTP_200_OK)
        return Response("Error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = AddRemoveFavoriteSerializer()
        return Response(serializer.data)

    
class ChargeWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response("There is not any customer with the given email" , status=status.HTTP_404_NOT_FOUND)
            customer.wallet_balance += serializer.validated_data['amount']
            customer.save()
            return Response({'email' : customer.email, 'wallet_balance':customer.wallet_balance}, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = WalletSerializer()
        return Response(serializer.data)
    
class WithdrawFromWalletView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response("There is not any customer with the given email" , status=status.HTTP_404_NOT_FOUND)
            if customer.wallet_balance - serializer.validated_data['amount'] >= 0:
                customer.wallet_balance -= serializer.validated_data['amount']
                customer.save()
            else:
                return Response("The wallet balance is insufficient" , status=status.HTTP_404_NOT_FOUND)
            return Response({'email' : customer.email, 'wallet_balance':customer.wallet_balance}, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = WalletSerializer()
        return Response(serializer.data)


class ShowAllCountry(APIView):
    def get(self, request):
        datas = Country.objects.all()
        serializer = CountrySerializer(datas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CitiesOfCountry(APIView):
    def post(self, request):
        country_name = request.data['name']
        country_id = Country.objects.get(name = country_name)
        cities = City.objects.filter(country_id = country_id)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get(self, request):
        serializer = CountrySerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)
class LatLongUpdateRetreive(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LatLongSerializer
    lookup_field = 'myauthor_ptr_id'
    lookup_url_kwarg = 'user_id'
    def get_queryset(self):
        print(self.kwargs)
        return Customer.objects.filter(id=self.kwargs['user_id'])

    def get_serializer_context(self):
        print(self.kwargs)
        return {'user_id': self.kwargs['user_id']}

    def patch(self, request, user_id):
        instance = get_object_or_404(Customer,myauthor_ptr_id = user_id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    
def get_lat_long(user_id):
    cust = get_object_or_404(Customer,id = user_id)
    content = JSONRenderer().render({'lat':cust.lat,'long':cust.lon})
    return HttpResponse(content, content_type='application/json')
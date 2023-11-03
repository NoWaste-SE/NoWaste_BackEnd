from django.contrib.auth import get_user_model,logout
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,generics,mixins,viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import  IsAdminOrReadOnly
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from .models import *
from .filters import RestaurantFilter , FoodFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
import requests
import json
from django.http import JsonResponse
import urllib
from django.core.serializers import serialize
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core import serializers
class ChangePasswordView(generics.UpdateAPIView):
    # queryset = Restaurant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        user = request.user
        if(user.id != self.kwargs['pk']):
            return Response({"message": "Unathorized!"},status=status.HTTP_401_UNAUTHORIZED)
        super().update(request, *args, **kwargs) 
        return Response({"message" :"Password changed successfully!"},status= status.HTTP_200_OK)


class RestaurantProfileViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    serializer_class = RestaurantSerializer
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class(*args, **kwargs)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class
    def get_serializer_context(self):
        return {'request': self.request}
    def get_object(self, id):
        try:
            return Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            raise Response(status= status.HTTP_404_NOT_FOUND)
    def list(self, request):
        queryset = Restaurant.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Restaurant.objects.get(id=id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
    def patch(self,request,id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

class RestaurantCustomerView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'


class FoodViewSet(ModelViewSet):
    serializer_class = FoodSerializer
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant__id'])


    def get_serializer_context(self):
        return {'restaurant_id': self.kwargs['restaurant__id']}
    # @action(detail=True, methods=['patch'])
    def patch(self, request, id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class ManagerFoodListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant_id'])


    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

    def create(self, request, *args, **kwargs):
        serializer = FoodSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ManagerFoodViewSet(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        print(self.kwargs)
        return Food.objects.filter(restaurant_id=self.kwargs['restaurant_id'])


    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

    def patch(self, request, id):
        instance = self.get_object(id= id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RestaurantSearchViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSearchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['rate', 'discount', 'name', 'date_of_establishment']

    def get_serializer_context(self):
        return {'request': self.request}
    

class FilterFoodViewSet(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodFilterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering_fields = ['price', 'name']

    def get_serializer_context(self):
        return {'request': self.request}


class RestaurantManagerListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

class RestaurantManagerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

class RestaurantManagerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RestaurantManager.objects.all()
    serializer_class = RestaurantManagerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = self.get_object()
        return context
    
class RestaurantManagerRestaurantListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        try:
            mang = RestaurantManager.objects.get(id=self.kwargs['manager_id'])
        except RestaurantManager.DoesNotExist:
            return Response("There is not any restaurant manager with the given id" , status=status.HTTP_404_NOT_FOUND)
        return self.queryset.filter(manager = mang)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = RestaurantManager.objects.get(pk = self.kwargs['manager_id'])
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                mang = RestaurantManager.objects.get(id=self.kwargs['manager_id'])
            except RestaurantManager.DoesNotExist:
                return Response("There is not any restaurant manager with the given id" , status=status.HTTP_404_NOT_FOUND)
            serializer.save(manager = mang)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class RestaurantManagerRestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['manager'] = RestaurantManager.objects.get(pk=self.kwargs['manager_id'])
        return context


class OrderAPIView(generics.RetrieveUpdateAPIView,generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetOrderSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Order.objects.filter(restaurant_id=self.kwargs['restaurant_id'] ,userId_id = self.kwargs['userId'],status = "notOrdered").prefetch_related('orderItems').select_related('userId').select_related('restaurant')
    
    def get_serializer_class(self, *args, **kwargs):
        return GetOrderSerializer

    def get_serializer_context(self):
        return {'restaurant_id': self.kwargs['restaurant_id'],'userId_id' : self.kwargs['userId']}
    
    def retrieve(self, request, *args, **kwargs):
        instance =  self.get_queryset().filter(restaurant_id=self.kwargs['restaurant_id'],userId_id = self.kwargs['userId']).exclude(Q(status='Completed') | Q(status='Ordered'))
        serializer = None
        if (instance.count() == 0) :
            print("hiii")
            instance = Order.objects.create(restaurant_id=self.kwargs['restaurant_id'],userId_id = self.kwargs['userId'])
            serializer = self.get_serializer(instance)
        else :
            serializer = self.get_serializer(instance,many = True)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# @login_required
def add_to_Order(request, *args, **kwargs):
    order  =  Order.objects.filter(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'],status = 'notOrdered').first()
    instance = order
    if(order is None):
        try :
            order = Order.objects.create(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'])
            instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
        except Exception as error:
            # handle the exception
            print("An exception occurred:", error) 
    else :
        instance = OrderItem.objects.filter(food_id = kwargs['food_id'], order_id = order.id).first()
        if (instance is None):
            try :
                instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
            except Exception as error:
            # handle the exception
                print("An exception occurred:", error)   
    food = Food.objects.get(id = kwargs['food_id'])    
    # user = Customer.objects.get(id = kwargs['userId'])
    try:  
        if food.remainder>0:
            instance.quantity = instance.quantity+ 1
            instance.save()  
            food.remainder -= 1
            food.save()
            # user.wallet_balance -= Decimal(serialized_data['name_and_price']['price'])
            # user.save()
    except Exception as error:
        # handle the exception
        print("An exception occurred:", error) 
    serializer = OrderItemSerializer(instance)
    serialized_data = serializer.data
    # serialized_data['new_wallet_balance'] = user.wallet_balance
    serialized_data['new_remainder'] = food.remainder

    content = JSONRenderer().render(serialized_data)
    return HttpResponse(content, content_type='application/json')

# @login_required
def remove_from_Order(request, *args, **kwargs):
    food = Food.objects.get(id = kwargs['food_id'])
    order  =  Order.objects.filter(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'],status = 'notOrdered').first()
    # instance = OrderItem.objects.create()
    instance = order
    context = {}
    if(order is None):
        data = {
            'name': food.name,
            'price': str(food.price),
            'message': "There is not any order between these user and restaurant",
            'new_remainder': food.remainder
        }

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json', status=status.HTTP_404_NOT_FOUND)
        # try:
        #     order = Order.objects.create(restaurant_id=kwargs['restaurant_id'],userId_id = kwargs['userId'])
        #     instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
        # except Exception as error:
        #     # handle the exception
        #     print("An exception occurred:", error) 
    else :
        instance = OrderItem.objects.filter(food_id = kwargs['food_id'], order_id = order.id).first()
        if (instance is None):
            data = {
            'name': food.name,
            'price': str(food.price),
            'message': "Customer didn't order this food",
            'new_remainder': food.remainder
            }

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json', status=status.HTTP_404_NOT_FOUND)
            # try:
            #     instance = OrderItem.objects.create(food_id = kwargs['food_id'], order_id = order.id)
            # except Exception as error:
            # # handle the exception
            #     print("An exception occurred:", error) 
    try:
        instance.quantity = instance.quantity- 1
        instance.save()
        if (instance.quantity <= 0):
            food.remainder += 1
            food.save()
            instance.delete()
            data = {
            'name': food.name,
            'price': str(food.price),
            'message': "The order item deleted from order",
            'new_remainder': food.remainder
            }
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json', status=status.HTTP_200_OK)
        
        # if(instance.quantity < 0) :
        #     instance.quantity = 0 
        # instance.save()
    except Exception as error:
    # handle the exception
        print("An exception occurred:", error) 
    serializer = OrderItemSerializer(instance)
    serialized_data = serializer.data
    # user = Customer.objects.get(id = kwargs['userId'])
    if instance.quantity > 0:
        food.remainder += 1
        food.save()
        # user.wallet_balance += Decimal(serialized_data['name_and_price']['price'])
        # user.save()
    # serialized_data['new_wallet_balance'] = user.wallet_balance
    serialized_data['new_remainder'] = food.remainder
    content = JSONRenderer().render(serialized_data)
    return HttpResponse(content, content_type='application/json')



class CustomerOrderViewAPI(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        return CustomerViewOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(userId_id=self.kwargs['user_id']).select_related('restaurant')
       
class RestaurantOrderViewAPI(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantOrderViewSerializer
    def get_queryset(self):
        queryset = Restaurant.objects.filter(manager_id = self.kwargs['manager_id']).prefetch_related('Orders')
        ordersList = []
        for restaurant in queryset:
            orders = restaurant.Orders.all()
            for order in orders:
                ordersList.append(order)
        return ordersList

class UpdateOrderStatusAPI(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'order_id'
    def get_serializer_class(self, *args, **kwargs):
        return UpdateOrderSerializer
    def get_queryset(self):
        return Order.objects.filter(id = self.kwargs['order_id'])
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


class CommentAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        writer = Customer.objects.get(id = kwargs['user_id'])
        restaurant = Restaurant.objects.get(id = kwargs['restaurant_id'])
        if serializer.is_valid(raise_exception=True):
            new_comment, created = Comment.objects.get_or_create(writer = writer, restaurant=restaurant)
            new_comment.text = serializer.validated_data['text']
            # serializer.save()
            new_comment.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        serializer = CommentSerializer()
        writer = Customer.objects.get(id = kwargs['user_id'])
        restaurant = Restaurant.objects.get(id = kwargs['restaurant_id'])
        try:
            comment = Comment.objects.get(writer=writer, restaurant=restaurant)
            return Response({'comment': comment.text}, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurantCommentListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # def get_queryset(self):
    #     restaurant_id = self.kwargs['restaurant_id']
    #     return Comment.objects.filter(restaurant_id=restaurant_id)
    def get(self, request, *args, **kwargs):
        restaurant_id = self.kwargs['restaurant_id']
        comments = Comment.objects.filter(restaurant_id=restaurant_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchNearestRestaurant(mixins.ListModelMixin):
    # serializer_class = RestaurantSerializer
    # @api_view(('GET',))
    # @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def search_nearest_restaurant(request):
    # def search_nearest_restaurant(request,origin):
        type_vehicle = 'car'
        origins = request.GET.get('origins')
        # destinations = '36.35067,59.5451965%7C36.337005,59.5300'
        # destinations = Restaurant.objects.values_list('lat', 'lon')
        restaurants = Restaurant.objects.all()
        # destinations = '%7C'.join([urllib.parse.quote(str(dest)) for dest in destinations])
        destinations = '|'.join([f"{restaurant.lat},{restaurant.lon}" for restaurant in restaurants])
        headers = {
            'Api-Key': 'service.f3f70682948d40999d64243013ff5b95',
        }
        print("*&&&&&&&&&&&&&&&&&&&&&&*",destinations)
        url = f'https://api.neshan.org/v1/distance-matrix/no-traffic?type={type_vehicle}&origins={origins}&destinations={destinations}'
        
        response = requests.get(url,headers= headers)
        data = response.json()
        print("########################",data)
        elements = data['rows'][0]['elements']
        destination_addresses = data['destination_addresses']
        dists = [element['distance']['value'] for element in elements]
        des_len = len(destination_addresses)
        des_dist_list = []
        for i in range(des_len):
            des_dist_list.append((elements[i]['distance']['value'],destination_addresses[i]))
        sorted_list = sorted(des_dist_list, key=lambda x: x[1])[:5]
        result = []
        for e in sorted_list:
            lat ,long = e[1].split(',')
            for rest in restaurants:
                if (rest.lat == lat,rest.lon == long):
                    result.append(rest)
        # serializer = RestaurantSerializer(result, many=True)
        data = serializers.serialize('json', result)
        return HttpResponse(data, content_type="application/json")
        # return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        return Response(serializer.data)
    # serializer =  RestaurantSerializer(result,many = True)
    # return HttpResponse(serializer.data,status = status.HTTP_200_OK)
        # return JsonResponse(sorted_list,safe= False)
    # serialized_data = serialize("json", result)
    # # serialized_data = json.loads(serialized_data)
    # return JsonResponse(serialized_data, safe=False, status=200)

def get_addr(request):
# def search_nearest_restaurant(request,origin):
    type_vehicle = 'car'
    Lattitude = request.GET.get('lat')
    longitude = request.GET.get('lng')
    destinations = '36.35067,59.5451965%7C36.337005,59.5300'
    # destinations = Restaurant.objects.values_list('lat', 'lon')
    # destinations = '%7C'.join([urllib.parse.quote(dest) for dest in destinations])

    headers = {
        'Api-Key': 'service.7f461dfe908a40899d8900c2802f48a0',
    }
    
    url = f'https://api.neshan.org/v5/reverse?lat={Lattitude}&lng={longitude}'
    
    response = requests.get(url,headers= headers)
    data = response.json()
    return JsonResponse(data,safe= False)

class LatLongUpdateRetreive(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LatLongSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'restaurant_id'
    def get_queryset(self):
        print(self.kwargs)
        return Restaurant.objects.filter(id=self.kwargs['restaurant_id'])

    def get_serializer_context(self):
        print(self.kwargs)
        return {'restaurant_id': self.kwargs['restaurant_id']}

    def patch(self, request, restaurant_id):
        instance = self.get_object(id= restaurant_id)
        for key , value in request.data.items():
            setattr(instance,key,value)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
def get_lat_long(request, *args, **kwargs):
    rest = get_object_or_404(Restaurant,id =kwargs['restaurant_id'])
    content = JSONRenderer().render({'lat':rest.lat,'long':rest.lon})
    return HttpResponse(content, content_type='application/json')

def test(request):
    return HttpResponse("test")

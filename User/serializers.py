from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *
from cities_light.models import Country, City
from Restaurant.models import Restaurant, Food, OrderItem2, Order2
from Restaurant.serializer import RestaurantSerializer, FoodSerializer
from django.contrib.auth.hashers import make_password

class BaseCreateUserSerializer(serializers.ModelSerializer): 
    role = serializers.CharField(max_length=255, default="default")
    code = serializers.CharField(max_length=10)
    class Meta: 
        abstract = True 
        model = Customer
        fields = ['name', 'password', 'email', 'role', 'code']
    def create(self, validated_data):
        role = validated_data.pop('role',None)
        code = validated_data.pop('code',None)
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CreateCustomerSerializer(BaseCreateUserSerializer): 
    class Meta(BaseCreateUserSerializer.Meta): 
        model = Customer
        fields = BaseCreateUserSerializer.Meta.fields


class CreateRestaurantSerializer(BaseCreateUserSerializer): 
    class Meta(BaseCreateUserSerializer.Meta): 
        model = RestaurantManager
        fields = BaseCreateUserSerializer.Meta.fields
    
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_Codes
        fields = ['name', 'email'] 


class MyAuthorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    class Meta:
        model = MyAuthor
        fields = ['password', 'email']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    role = serializers.CharField(max_length=255, default="default")
    class Meta:
        model = Customer
        fields = ['name', 'password', 'email', 'role']
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name','address','username','email','phone_number','gender','date_of_birth','wallet_balance']
        extra_kwargs = {
            'address': {'required': False, 'allow_blank': True},
            'name' : {'required': False, 'allow_blank': True},
            'email' : {'read_only': True}
        }
class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = MyAuthor
        fields = ['email']

class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    code = serializers.CharField(max_length=10, required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = MyAuthor
        fields = ['email', 'code']

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True,source = 'password')

    class Meta:
        model = MyAuthor
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value


    def update(self, instance, validated_data):
        user = self.context['request'].user
        #  user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError({"authorize": "You must be logged in to perform this action."})

        if user.pk != self.instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'role', 'email' ,'address','wallet_balance','gender','phone_number','date_of_birth','lat','lon','password')
        extra_kwargs = {
            'wallet_balance': {'read_only': True},
            'name' : {'required': False, 'allow_blank': True},
            'email' : {'required': False,'allow_null': True},
            'address' : {'required': False,'allow_null': True}
        }

    def validate_email(self, new_email):
        user = self.context['request'].user
        if Customer.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return new_email

    def validate_username(self, value):
        user = self.context['request'].user
        if Customer.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        # Customer.objects.filter(id = instance.id).update(username='some value')
        print("******************************")
        print(instance)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.wallet_balance = validated_data.get('wallet_balance', instance.wallet_balance)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.role = validated_data.get('role', instance.role)
        # password = validated_data.get('password',instance.password)
        # if password:
        #     instance.set_password(password)
        instance.save()
        return instance
    
class RateRestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])
    class Meta:
        model = Restaurant
        fields = ['rate', 'name']

class AddRemoveFavoriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])
    email = serializers.EmailField(validators=[])
    class Meta:
        model = Restaurant
        fields = ['email', 'name']


class RestaurantSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'discount', 'rate']

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[])
    amount = serializers.DecimalField(decimal_places=2, max_digits= 20)
    class Meta:
        model = Customer
        fields = ['email', 'amount']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']
    def to_representation(self, instance):
        return instance.name
    
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']
    def to_representation(self, instance):
        return instance.name
    
class LatLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['lat','lon']
        
        
class OrderItemSerializer2(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=['plus', 'minus'], default='plus')
    
    class Meta:
        model = OrderItem2
        fields = ['action', 'item', 'order']
        read_only_fields = ['order']
        
    def validate(self, attrs):
        action = attrs.get('action')
        item = attrs.get('item')
        user = self.context['request'].user
        customer = Customer.objects.get(myauthor_ptr_id=user.id)
        restaurant = Food.objects.filter(id=item.id).first().restaurant
        if action == 'minus' and not OrderItem2.objects.filter(order=Order2.objects.get_InProgress_order(customer, restaurant), item=item).exists():
            raise serializers.ValidationError('You have no such item in your order')
        if action == 'plus' and Food.objects.get(id=item.id).remainder <= 0:
            raise serializers.ValidationError('This item is not available now')
        return attrs
        
    def create(self, validated_data):
        item = validated_data.get('item')
        action = validated_data.get('action')
        user = self.context['request'].user
        customer = Customer.objects.get(myauthor_ptr_id=user.id)
        restaurant = Food.objects.filter(id=item.id).first().restaurant
        order_item = Order2.objects.get_InProgress_order(customer, restaurant).update_items(item, action)
        return order_item
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['quantity'] = instance.quantity
        data['total_price'] = instance.total_price
        data['total_price_after_discount'] = instance.total_price_after_discount
        data['item'] = FoodSerializer(instance.item).data
        return data
        

class OrderSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Order2
        fields = ['id', 'status', 'order_date', 'customer', 'restaurant', 'total_price']
        read_only_fields = ['customer', 'restaurant', 'status', 'id', 'order_date', 'total_price']
        
    def get_items(self, order):
        return OrderItemSerializer2(OrderItem2.objects.filter(order=order), many=True).data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = instance.total_price
        data['total_price_after_discount'] = instance.total_price_after_discount
        data['restaurant'] = RestaurantSerializer(instance.restaurant).data
        data['items'] = OrderItemSerializer2(OrderItem2.objects.filter(order=instance), many=True).data
        return data
    
class TempManagerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    class Meta:
        model = TempManager
        fields =  ['email','name','id']

class ManagerSerialzer(serializers.ModelSerializer):
    
    def get_restaurants(self,resmng):
        return RestaurantSerializer(Restaurant.objects.filter(manager = resmng),many = True).data

    restaurants = serializers.SerializerMethodField()
    class Meta : 
        model = RestaurantManager
        fields = ['name','email','number','manager_image','lat','lon','restaurants']


 
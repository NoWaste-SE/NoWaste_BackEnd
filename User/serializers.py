from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from .models import *
# from Restaurant.serializer import RestaurantSerializer



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
    # password = serializers.CharField(write_only=True, style={'input_type': 'password'},
    #                             required=True, allow_blank=False, allow_null=False,
    #                             validators=[validate_password])
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
    # role = serializers.CharField()
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

    # def validate_old_password(self, value):
    #     user = self.context['request'].user

    #     if isinstance(user, AnonymousUser):
    #         return value

    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})

    #     return value

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
        fields = ('username', 'name', 'email' ,'address','wallet_balance','gender','phone_number','date_of_birth','lat','lon')
        extra_kwargs = {
            'wallet_balance': {'read_only': True},
            'username' :{'required' : False, 'allow_blank': True},
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
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)

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


# class CountryCityDictSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CountryCityDict
#         fields = '__all__'

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
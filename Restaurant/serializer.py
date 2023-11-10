from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from User.models import Restaurant ,Customer, RestaurantManager
from User.serializers import MyAuthorSerializer
from .models import *

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        address = serializers.CharField(source = 'address')
        fields = ('number','name','address','rate','discount','date_of_establishment','description','restaurant_image','id', 'type','lat','lon','manager_id')

        extra_kwargs = {
            'address': {'required': False},
            'name' : {'required': False},
        }
    
    def validate_email(self, new_email):
        user = self.context['request'].user
        if Restaurant.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return new_email


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_establishment = validated_data.get('date_of_establishment', instance.date_of_establishment)
        instance.description = validated_data.get('description', instance.description)
        instance.restaurant_image = validated_data.get('restaurant_image', instance.restaurant_image)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True,source = 'password')

    class Meta:
        model = RestaurantManager
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

        if not user.is_authenticated:
            raise serializers.ValidationError({"authorize": "You must be logged in to perform this action."})

        if user.pk != self.instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class RestaurantSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'discount', 'rate', 'date_of_establishment', 'id', 'address', 'number', 'restaurant_image']
        lookup_field = 'id'

class FoodFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'price', 'ingredients', 'food_pic', 'food_pic2', 'restaurant', 'remainder']
        lookup_field = 'id'

class FoodSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(read_only = False)
    class Meta :
        model = Food
        fields = ['name','price','ingredients','food_pic', 'food_pic2', 'restaurant_id','id', 'remainder']


class RestaurantManagerSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many = True, read_only=True)
    class Meta:
        model = RestaurantManager
        fields = ['id', 'name','email','restaurants','number', 'manager_image']

    def create(self, validated_data):
        restaurants_data = validated_data.pop('restaurants',[])
        manager = RestaurantManager.objects.create(**validated_data)
        for res_data in restaurants_data:
            Restaurant.objects.create(manager = manager, **res_data)
        return manager
    
    def update(self, instance, validated_data):
        restaurants_data = validated_data.pop('restaurants', [])
        for res_data in restaurants_data:
            res_id = res_data.get('id', None)
            if res_id:
                restaurant = instance.restaurants.filter(id=res_id).first()
                if restaurant:
                    restaurant.name = res_data.get('name', restaurant.name)
                    restaurant.save()
                else:
                    Restaurant.objects.create(manager=instance, **res_data)
            else:
                Restaurant.objects.create(manager=instance, **res_data)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.number = validated_data.get('number', instance.number)
        instance.manager_image = validated_data.get('manager_image', instance.manager_image)
        instance.save()
        return instance
class SimpleFoodSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Food
        fields = ['name','price']

class OrderItemSerializer(serializers.ModelSerializer):
    def get_name_and_price(self,orderitem):
        return SimpleFoodSerializer(orderitem.food).data
    name_and_price = serializers.SerializerMethodField()
    new_remainder = serializers.IntegerField(read_only=True)
    class Meta : 
        model = OrderItem
        fields = ('quantity', 'new_remainder','name_and_price')

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Restaurant
        fields = ['name','address','logo','number','id']

class GetOrderSerializer(serializers.ModelSerializer):
    def get_Subtotal_Grandtotal_discount(self, order:Order):
        quantities = []
        price = []
        discount = 0
        Grandtotal = 0
        Subtotal = 0
        for item in order.orderItems.all():
            price.append(item.quantity * item.food.price)
            quantities.append(item.quantity)
        Subtotal = sum(price)
        Grandtotal = Subtotal
        if order.restaurant.discount == 0:
            discount = 0
        elif sum(quantities) < order.restaurant.purches_counts:
            discount = 0
        else : 
            discount = order.restaurant.discount
        if (discount != 0):
            Grandtotal =(1-discount) * Subtotal
        return Subtotal,Grandtotal,discount

    def get_userAddress(self,order :Order):
        return order.userId.address

    def get_restaurantDetails(self,order):
        return SimpleRestaurantSerializer(order.restaurant).data
    
    orderItems = OrderItemSerializer(many=True, read_only=True)
    userAddress = serializers.SerializerMethodField()
    restaurantDetails = serializers.SerializerMethodField()
    class Meta : 
        model = Order
        fields = ('id','orderItems','restaurantDetails','userAddress','status')

        extra_kwargs = {
        'orderItems': {'read_only': True},
        'discount': {'read_only': True},
        'total_price': {'read_only': True}
        }

class CustomerViewOrderSerializer(serializers.ModelSerializer):
    def get_orderDetails(self,order):
        return GetOrderSerializer(order).data
    def get_restaurantDetails(self,order):
        return SimpleRestaurantSerializer(order.restaurant).data
    orderDetails = serializers.SerializerMethodField()  # Embedding ParentSerializer in ChildSerializer
    restaurantDetails = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta : 
        model = Order
        fields = ['orderDetails','restaurantDetails','status','created_at']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customer
        fields = ['name','phone_number','address','username','email']
class RestaurantOrderViewSerializer(serializers.ModelSerializer):
    def get_orderDetails(self,order):
        return GetOrderSerializer(order).data
    
    def get_userDetails(self,order):
        return SimpleUserSerializer(order.userId).data
    
    orderDetails = serializers.SerializerMethodField()  # Embedding ParentSerializer in ChildSerializer
    userDetails = serializers.SerializerMethodField()
    status = serializers.CharField()
    class Meta : 
        model = Order
        fields = ['orderDetails','userDetails','status','created_at']
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Order
        fields = ['status']



class CommentSerializer(serializers.ModelSerializer):

    def get_created_at_date(self, comment :Comment):
        return str(comment.created_at)[:10]
    writer_username = serializers.CharField(source='writer.username', read_only=True)
    created_at_date = serializers.SerializerMethodField(read_only=True)
    class Meta : 
        model = Comment
        fields = ['text', 'writer_username', 'created_at_date']

class LatLongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['lat','lon']
        
        
class OrderItemSerializer2(serializers.ModelSerializer):
    class Meta:
        model = OrderItem2
        fields = ['quantity', 'item']
        read_only_fields = ['order']
        
    def create(self, validated_data):
        item = validated_data.get('item')
        quantity = validated_data.get('quantity')
        user = self.context['request'].user
        customer = Customer.objects.get(myauthor_ptr_id=user.id)
        restaurant = Food.objects.filter(id=item.id).first().restaurant
        order = Order2.objects.get_initiated_order(restaurant, customer).update_items(item, quantity)
        return order

class OrderSerializer2(serializers.ModelSerializer):
    items = OrderItemSerializer2(many=True, read_only=True)

    class Meta:
        model = Order2
        fields = '__all__'
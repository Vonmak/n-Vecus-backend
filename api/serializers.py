from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from core.models import *
from accounts.models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    class Meta:
        model = get_user_model()
        fields =('username','email','password','roles','phone')
        extra_kwargs = {'password':{'write_only':True,'min_length':6}}

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields ='__all__'
            
class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model= Vendor
        fields ='__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='items-detail')
    user = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields="__all__"
          
class OrderItemSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='orderitem-detail')
    user = UserSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields="__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    user = UserSerializer(read_only=True)
    class Meta: 
        model=Order
        fields="__all__"
        
class TransactionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transaction-detail')
    user = UserSerializer(read_only=True)
    class Meta:
        model= Transaction
        fields="__all__"
        
        
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False
    )
    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid User Credentials")
        attrs['user'] =user
        
        return attrs
  
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from payments.models import Transaction
from .serializers import *
from core.models import *

from django.contrib.auth import login

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args,**kwargs):
        serializers=AuthTokenSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        refresh = RefreshToken.for_user(user)
        login(request, user)
        
        return Response({
            'username': user.username,
            'id': user.id,
            'email': user.email,
            'roles': user.roles,
            'phone': user.phone,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class CustomerViewset(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Customer.objects.get(user=user)
        print(profile)
        data = CustomerSerializer(profile, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user= request.user
        profile = Customer.objects.get(user=user)
        print(profile)
        serializer = CustomerSerializer(profile,data=request.data, context={'request': request},partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    
class VendorViewset(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        profile = Vendor.objects.get(user=user)
        print(profile)
        data = VendorSerializer(profile, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user= request.user
        profile = Vendor.objects.get(user=user)
        print(profile)
        serializer = VendorSerializer(profile,data=request.data, context={'request': request},partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)

class ProductViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.vendor)

class OrderItemViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset= OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customer)
    
class OrderViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customer)

class TransactionViewset(viewsets.ModelViewSet):
    permissions= IsAuthenticated
    queryset= Transaction.objects.all()
    serializer_class= TransactionSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customer)

class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # print(request.data)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
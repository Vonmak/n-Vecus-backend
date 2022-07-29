from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import *
from django.urls import path


router = DefaultRouter()
router.register('items', ProductViewset, basename='items')
router.register('orderitem', OrderItemViewset, basename='orderitem')
router.register('order', OrderViewset, basename='order')
router.register('transaction', TransactionViewset, basename='transaction')


urlpatterns=[
    path('signup/',CreateUserView.as_view(),name='signup'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('customer/', CustomerViewset.as_view(), name='customer'),
    path('vendor/', VendorViewset.as_view(), name='vendor'),
]

urlpatterns += router.urls
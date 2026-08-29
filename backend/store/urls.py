from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    # auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/update/<int:item_id>/', views.CartUpdateView.as_view(), name='cart-update'),
    path('cart/remove/<int:item_id>/', views.CartRemoveView.as_view(), name='cart-remove'),

    # orders
    path('orders/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),

    # razorpay online payment
    path('orders/razorpay/create/', views.RazorpayCreateOrderView.as_view(), name='razorpay-create'),
    path('orders/razorpay/verify/', views.RazorpayVerifyView.as_view(), name='razorpay-verify'),
]

import razorpay
from django.conf import settings
from django.db import transaction
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    RegisterSerializer, CategorySerializer, ProductSerializer,
    CartSerializer, OrderSerializer, CheckoutSerializer,
    RazorpayCreateOrderSerializer, RazorpayVerifySerializer,
)


def _create_order_from_cart(user, cart, shipping_address, payment_method, payment_status):
    """Shared helper: turns the current cart into an Order + OrderItems, then empties the cart."""
    order = Order.objects.create(
        user=user,
        shipping_address=shipping_address,
        total_price=cart.total_price,
        payment_method=payment_method,
        payment_status=payment_status,
    )
    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        )
        item.product.stock = max(item.product.stock - item.quantity, 0)
        item.product.save()
    cart.items.all().delete()
    return order


# ---------- Auth ----------

class RegisterView(generics.CreateAPIView):
    """POST username, email, password -> creates a user + empty cart."""
    queryset = None
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ---------- Categories & Products (read-only for everyone, browsable without login) ----------

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        if search:
            qs = qs.filter(name__icontains=search)
        if category:
            qs = qs.filter(category__slug=category)
        return qs


# ---------- Cart (requires login) ----------

class CartView(APIView):
    """GET the logged-in user's cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)


class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product,
                                                         defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        quantity = int(request.data.get('quantity', 1))
        item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
        if not item:
            return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)


class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
        if item:
            item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)


# ---------- Orders (requires login) ----------

class CheckoutView(APIView):
    """Cash on Delivery checkout: turns the current cart into an Order right away."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = _create_order_from_cart(
                user=request.user,
                cart=cart,
                shipping_address=serializer.validated_data['shipping_address'],
                payment_method='cod',
                payment_status='pending',
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# ---------- Razorpay online payment (requires login) ----------

class RazorpayCreateOrderView(APIView):
    """
    Step 1 of online payment: create a Razorpay order for the cart's current total.
    Does NOT touch our own Order table yet - that happens after payment is verified.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RazorpayCreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            return Response(
                {'detail': 'Razorpay is not configured on the server. '
                           'Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET (see README).'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(cart.total_price * 100)

        razorpay_order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': 1,
        })

        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount_in_paise,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
        })


class RazorpayVerifyView(APIView):
    """
    Step 2: called by the frontend after the Razorpay checkout popup succeeds.
    Verifies the payment signature, then creates the real Order and empties the cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RazorpayVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature'],
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({'detail': 'Payment verification failed.'},
                             status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = _create_order_from_cart(
                user=request.user,
                cart=cart,
                shipping_address=data['shipping_address'],
                payment_method='razorpay',
                payment_status='paid',
            )
            order.razorpay_order_id = data['razorpay_order_id']
            order.razorpay_payment_id = data['razorpay_payment_id']
            order.razorpay_signature = data['razorpay_signature']
            order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

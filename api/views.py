
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CategorySerializer, BrandSerializer, ProductSerializer, CustomUserSerializer, \
    EmailAuthTokenSerializer, CartSerializer, OrderSerializer
from backend.models import Category, Brand, Product, CustomUser, Cart, Order
from backend.models import Category, Brand, Product, CustomUser
from rest_framework.authtoken.models import Token




class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "User successfully registered"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):

    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        # return Response({
        #     'token_type':'token',
        #     'token':token.key,
        #     'user_id':user.pk,
        #     'email':user.email
        # })

        return  Response(token.key)

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]  # User must be logged in via token

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


# Create your views here.
class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }

        return Response(data)

class BrandListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer =self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }
        return Response(data)

class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data" : serializer.data
        }
        return Response(data)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_id = request.user.id

        carts = Cart.objects.filter(custom_user_id = customer_id)

        transformed_carts = CartSerializer(carts, many=True, context={'request': request}).data

        grand_total = Cart.grand_total(customer_id)

        return Response({'data': transformed_carts, 'grand_total': grand_total}, status=status.HTTP_200_OK)

    def post(self, request):
        customer_id = request.user.id
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)

        existing_cart_item = Cart.objects.filter(product_id=product_id, custom_user_id=customer_id).first()

        if existing_cart_item:
            existing_cart_item.qty +=1
            existing_cart_item.save()
            return Response({"message": f"{product.name} quantity updated in your cart"}, status=status.HTTP_201_CREATED)
        else:
            Cart.objects.create(product_id=product_id, customer_id=customer_id, qty=1)
            return Response({"message": f"{product.name} added to your cart."}, status=status.HTTP_201_CREATED)


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        customer_id = request.user.id
        cart_item_id = request.data.get('cart_id')

        cart_item = Cart.objects.get(id=cart_item_id)

        if not cart_item:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.custom_user_id != customer_id:
            return Response({"error": "you are not authorized to remove this item  from the cart."}, status=status.HTTP_403_FORBIDDEN)

        cart_item.delete()
        return Response({"message": "Item removed from your cart."}, status=status.HTTP_200_OK)

    def patch(self, request):
        customer_id = request.user.id
        cart_item_id = request.data.get('cart_id')
        action = request.data.get('action')

        cart_item = Cart.object.get(id=cart_item_id)

        if not cart_item:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.custom_user_id != customer_id:
            return Response({"error": "You are not authorized to update the quantity of this item in the cart."},
                            status=status.HTTP_403_FORBIDDEN)

        if action == "increase":
            cart_item.qty += 1
        elif action == "decrease":
            cart_item.qty = max(cart_item.qty - 1, 1)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()
        return Response({"message": "Quantity updated in your cart."}, status=status.HTTP_200_OK)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        customer_id = request.user.id
        Cart.objects.filter(custom_user_id=customer_id).delete()
        return Response({"message": "cart cleared successfully"}, status=status.HTTP_200_OK)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_id = request.user.id
        # carts = Cart.objects.filter(custom_user_id=customer_id)
        orders = Order.objects.filter(custom_user_id=customer_id).order_by('id')
        serializer = OrderSerializer(orders, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order placed successfully."}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Order Creation failed', 'message': serializer.error}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Order update failed', 'message': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
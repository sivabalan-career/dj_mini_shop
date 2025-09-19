from logging import raiseExceptions
from os.path import exists

from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CategorySerializer, BrandSerializer, ProductSerializer, CustomUserSerializer, \
    EmailAuthTokenSerializer, CartSerializer
from backend.models import Category, Brand, Product, CustomUser, Cart
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


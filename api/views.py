from logging import raiseExceptions

from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CategorySerializer, BrandSerializer, ProductSerializer, CustomUserSerializer, \
    EmailAuthTokenSerializer
from backend.models import Category, Brand, Product, CustomUser
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
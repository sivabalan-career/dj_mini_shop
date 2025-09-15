from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CategorySerializer, BrandSerializer, ProductSerializer
from backend.models import Category, Brand, Product


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
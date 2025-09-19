from django.urls import path

from api.views import CategoryListView, BrandListView, ProductListView

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='category_list'),
    path('brands', BrandListView.as_view(), name='brand_list'),
    path('products', ProductListView.as_view(), name='brand_list')

    ]
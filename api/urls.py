from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import CategoryListView, BrandListView, ProductListView, UserCreateAPIView, CustomAuthToken, \
    UserInfoAPIView

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

    # Login Type 1
    path('token', obtain_auth_token, name='api_token_auth'),

    # Login Type 2
    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),

    path('user', UserInfoAPIView.as_view(), name='user-info'),

    path('categories', CategoryListView.as_view(), name='category_list'),
    path('brands', BrandListView.as_view(), name='brand_list'),
    path('products', ProductListView.as_view(), name='brand_list')

]
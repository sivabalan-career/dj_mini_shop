from django.urls import path

from api.views import CategoryListView

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='category_list')
]
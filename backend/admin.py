from django.contrib import admin
from django.contrib.admin import register

from backend.models import Category, Brand


# Register your models here.
@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
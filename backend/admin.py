from django.contrib import admin
from django.contrib.admin import register

from backend.models import Category


# Register your models here.
@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
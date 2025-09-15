from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "category"

class Brand(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "brand"

class Product(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length=255)
    # price = models.DecimalField(max_length=10, max_digits=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'product'
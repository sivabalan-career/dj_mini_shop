from idlelib.sidebar import get_end_linenumber
from multiprocessing.util import abstract_sockets_supported

from django.contrib.admin.actions import delete_selected
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from backend.manager import CustomerUserManager


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class GenderedImageField(models.ImageField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value or not hasattr(model_instance,self.attname):

            gender = model_instance.gender if hasattr(model_instance,'gender')else Gender.MALE

            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.jpg'
            else:
                value = 'profile/default_image.png'

        elif model_instance.gender != getattr(model_instance,f"{self.attname}_gender_cache",None):
            gender = model_instance.gender
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                value = 'profile/default_image.jpg'
        setattr(model_instance,f"{self.attname}_gender_cache",model_instance.gender)
        return value

class CustomUser(AbstractUser):

    username = None

    email = models.EmailField(_('email address'), unique=True)

    gender = models.CharField(max_length=1, choices=Gender.choices,default=Gender.MALE)

    image = GenderedImageField(upload_to='profile/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']
    objects = CustomerUserManager()

    def __str__(self):
        return self.email


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



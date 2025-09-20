import hashlib

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from backend.models import Category, Brand, Product, CustomUser, Cart, OrderItem, Order


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.SerializerMethodField()  # <-- Add avatar field

    class Meta:
        model = CustomUser
        fields = [
            'name',
            'gender',
            'password',
            'email',
            'avatar',
        ]

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        # group = Group.objects.get(name='EMPLOYEE')
        # user.groups.add(group)
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

    read_only_fields = ['avatar']

    def get_avatar(self, obj):
        """
        Generate Gravatar URL based on user's email
        """
        email = obj.email.strip().lower()
        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        return f"https://gravatar.com/avatar/{email_hash}"

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_customer_name(self, obj):
        return obj.product.id if obj.product else None

    def get_product_id(self, obj):
        return obj.product.id if obj.product else None

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def get_product_image(self, obj):
        if obj.product and obj.product.images.exists():
            request = self.context.get('request')
            image_url = obj.product.images.first().image.url
            return request.build_absolute_uri(image_url) if request else image_url
        return None

    def get_price(self, obj):
        return obj.product.price if obj.product else None

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','qty',"unit_price",'amount','discount']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'order_status', 'payment_method', 'order_items']
        read_only_fields = ['customer']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')

        user = self.context['request'].user
        order = Order.objects.create(customer=user, **validated_data)
        total_amount = 0

        for item_data in order_items_data:

            amount = item_data['qty'] * item_data['unit_price']
            total_amount += amount

            OrderItem.objects.create(

                order = order,
                product = item_data['product'],
                qty = item_data['qty'],
                unit_price = item_data['unit_price'],
                amount = item_data['amount'],
                discount = item_data['discount']
            )

            order.total_amount = total_amount
            order.save()
            return order



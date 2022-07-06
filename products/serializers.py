from dataclasses import fields
from rest_framework import serializers

from user.serializers import SellerSerializer
from .models import Product
from user.models import User
from rest_framework.mixins import CreateModelMixin

class CreateProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ListProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from products.permissions import IsOwnerPermission, IsSellerOrGetPermission

from products.serializers import CreateProductsSerializer, ListProductsSerializer
from .models import Product
from utils.mixins import SerializerByMethodMixin

# Create your views here.

class CreateListProductsView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrGetPermission]

    queryset = Product.objects.all()
    serializer_map = {
        'GET': ListProductsSerializer,
        'POST': CreateProductsSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class UpdateListOneProductView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrGetPermission, IsOwnerPermission]

    queryset = Product.objects.all()
    serializer_map = {
        'GET': ListProductsSerializer,
        'PATCH': CreateProductsSerializer,
    }
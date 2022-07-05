from django.contrib.auth import authenticate
from django.shortcuts import render

from rest_framework import generics 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import User
from .serializers import AccountSerializer, LoginSerializer

# Create your views here.

class AccountsView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

class AccountsNewestView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.kwargs['num']
        return self.queryset.order_by('-id')[0:num]

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        verify = serializer.is_valid()

        if not verify:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user:

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})

        return Response({"detail":"invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
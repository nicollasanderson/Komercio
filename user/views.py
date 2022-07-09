from django.contrib.auth import authenticate

from rest_framework import generics 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import User
from .serializers import AccountSerializer, ActiveDeactiveSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import IsSuperUserPermission, IsUserOwnerPermission

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

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOwnerPermission]

class ActivedeactivateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ActiveDeactiveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserPermission]
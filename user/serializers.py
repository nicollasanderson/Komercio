from rest_framework import serializers
from django.utils import timezone
from .models import User

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','is_seller','date_joined','password']
        read_only_fields = ['date_joined']
        write_only_fields = ['password']

    def create(self, validated_data):

        validated_data['date_joined'] = timezone.now()
        validated_data['username'] = validated_data['email']

        user = User.objects.create(**validated_data)        

        user.set_password(validated_data['password'])

        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
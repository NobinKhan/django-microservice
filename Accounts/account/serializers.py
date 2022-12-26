from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'is_active', 'is_deleted')
        extra_kwargs = {
            'phone': {'required': True},
        }


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'date_of_birth', 'gender', 'photo')
        extra_kwargs = {
            'user': {'required': True},
            'name': {'required': True}
        }


class RegisterUserSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ('user', 'name',)
        extra_kwargs = {
            'user': {'required': True},
            # 'name': {'required': True}
        }
    
    def is_valid(self, *, raise_exception=False):
        self.initial_data = {
            'user': {'phone':self.initial_data.get('phone')},
            'name': self.initial_data.get('name'),
        }
        return super().is_valid(raise_exception=raise_exception)
    
    
    # def validate(self, attrs):
    #     print(f"in validation = {attrs}")
    #     return attrs

    # def save(self, **kwargs):
    #     print(f"in save = {self.validated_data}")
    #     return super().save(**kwargs)


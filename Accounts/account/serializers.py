from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import Profile
from functions.handle_error import get_object_or_None

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


class RegisterUserSerializer(Serializer):
    phone = CharField(max_length=17)
    name = CharField(max_length=250)

    class Meta:
        fields = ('phone', 'name',)
        extra_kwargs = {
            'phone': {'required': True},
            'name': {'required': True}
        }
    
    def save(self, **kwargs):
        user = UserSerializer(data={'phone': self.initial_data.get('phone')})
        if not user.is_valid():
            self._errors = user._errors
            if self._errors:
                raise ValidationError(self.errors)
            return not bool(self._errors)
        user.save()

        profile = ProfileSerializer(data={'user':user.instance.id, 'name':self.initial_data.get('name')})
        if not profile.is_valid():
            user.instance.delete()
            self._errors = profile._errors
            if self._errors:
                raise ValidationError(self.errors)
            return not bool(self._errors)
        profile.save()
        return user.instance
    


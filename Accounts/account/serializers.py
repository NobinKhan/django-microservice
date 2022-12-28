from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.settings import api_settings
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Profile, OTPtoken
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
    

class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"] = PhoneNumberField(required=True)
        self.fields["token"] = IntegerField(required=True)
        self.fields[self.username_field] = CharField(required=False)
        self.fields["password"] = PasswordField(required=False)

    
    @classmethod
    def get_token(cls, user):
        # token = super().get_token(user)
        # # Add custom claims
        # token['name'] = user.name
        return super().get_token(user)
    
    def verify_token(self):
        otp_obj = get_object_or_None(OTPtoken, token=self.initial_data.get('token'), is_active=True)
        if not otp_obj:
            raise ValidationError({
                "token": [
                "Invalid OTP Token"
            ]})

        if otp_obj.type == 'Others':
            otp_obj.is_active = False
            otp_obj.save()
        elif otp_obj.type == 'Register' and otp_obj.user.phone == self.user.phone:
            self.user.is_active = True
            self.user.save()
            otp_obj.delete()
        elif otp_obj.type == 'Login' and otp_obj.user.phone == self.user.phone:
            otp_obj.delete()
        else:
            raise ValidationError({
                "token": [
                "Invalid OTP Token"
            ]})
    
    def validate(self, attrs):
        if attrs.get('phone') and attrs.get('token'):
            attrs[self.username_field] = str(attrs.get('phone'))
            attrs["password"] = str(attrs.get('token'))
            self.user = get_object_or_None(User, username=attrs.get('username'), phone=attrs.get('phone'))
            self.verify_token()
        
        data = {}
        refresh = self.get_token(self.user)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # Add extra responses here
        # data['username'] = self.user.username
        # data['groups'] = self.user.groups.values_list('name', flat=True)
        return data
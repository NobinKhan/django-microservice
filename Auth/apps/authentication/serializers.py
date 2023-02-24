from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from phonenumber_field.serializerfields import PhoneNumberField

from apps.common.utils import get_object
from apps.users.models import OTPtoken
from apps.token.tokens import AccessToken
from apps.token.authentication import default_user_authentication_rule
from apps.token.settings import api_settings
from apps.token.tokens import AccessToken


UPDATE_LAST_LOGIN = False


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)


class OutputAccessTokenSerializer(serializers.Serializer):
    """
    Output Access Token For Users.
    You Can Only Get Access Token For Active Users.
    """
    username_field = get_user_model().USERNAME_FIELD
    # token_class = None
    token_class = AccessToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(required=False)
        self.fields["phone"] = PhoneNumberField(required=True)
        self.fields["token"] = serializers.IntegerField(required=True)
        self.fields["password"] = PasswordField(required=False)

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

    def verify_otp(self):
        # otp_obj = get_object(OTPtoken, user=self.user, is_used=False)
        otp_obj = OTPtoken.objects.filter(user=self.user, is_used=False).last()
        if not otp_obj:
            otp_obj = get_object(OTPtoken, token=self.initial_data.get('token'), is_used=False)
        if not otp_obj:
            raise ValidationError({
                "token": [
                "Invalid OTP Token"
            ]})

        if otp_obj.perpose == OTPtoken.Perpose.OTHER:
            otp_obj.is_used = True
            otp_obj.save()
        elif otp_obj.perpose == OTPtoken.Perpose.REGISTER and otp_obj.user.phone == self.user.phone and self.user.is_active == False:
            self.user.is_active = True
            self.user.save()
            otp_obj.delete()
        elif otp_obj.perpose == OTPtoken.Perpose.LOGIN and otp_obj.user.phone == self.user.phone and self.user.is_active == True:
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
            self.user = get_object(get_user_model(), username=attrs.get('username'), phone=attrs.get('phone'))

        if not default_user_authentication_rule(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        self.verify_otp()
        
        data = {}
        token = self.get_token(self.user)
        if UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        data["access"] = str(token)

        return data


# class TokenVerifySerializer(serializers.Serializer):
#     token = serializers.CharField()

#     def validate(self, attrs):
#         token = UntypedToken(attrs["token"])

#         if (
#             api_settings.BLACKLIST_AFTER_ROTATION
#             and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
#         ):
#             jti = token.get(api_settings.JTI_CLAIM)


#         return {}


# class TokenBlacklistSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
#     token_class = RefreshToken

#     def validate(self, attrs):
#         refresh = self.token_class(attrs["refresh"])
#         try:
#             refresh.blacklist()
#         except AttributeError:
#             pass
#         return {}

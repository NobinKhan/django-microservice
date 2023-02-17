from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from apps.api.mixins import ApiAuthMixin
from apps.authentication.services import auth_logout
from apps.users.selectors import user_get_login_data


class SendOTP(APIView):
    def get(self, request):
        # Verifying request
        phone = request.query_params.get('phone')
        if not phone:
            return Response({"error":"'phone' param is required. It can't be empty or null."}, status=status.HTTP_404_NOT_FOUND)
        
        error, phone, error_code = verify_phone(phone=phone.replace(" ", "+"))
        if error:
            return Response({"error":phone}, status=error_code)
        
        error, user, error_code = verify_user(phone=phone)
        if error:
            return Response({"error":user}, status=error_code)
        if user.is_deleted:
            return Response({"error":"User Not Found With The Given Phone Number"}, status=status.HTTP_404_NOT_FOUND)
        
        # Time limite to send OTP again
        old_otp = OTPtoken.objects.filter(user=user)
        if old_otp:
            difference = timezone.now() - old_otp[0].created
            if difference.total_seconds() < 60:
                return Response({"message": f"Please wait {int(60-difference.total_seconds()+2)} seconds to get another OTP"}, status=status.HTTP_204_NO_CONTENT)

        # Sending OTP Code
        if user.is_active:
            saving_otp_token(type='Login', user=user)
        else:
            saving_otp_token(type='Register', user=user)
        return Response({"message": f"OTP verification code sent to this {user.phone} number."}, status=status.HTTP_202_ACCEPTED)



'''

class UserSessionLoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({"session": session_key, "data": data})


class UserSessionLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        # We are redefining post so we can change the response status on success
        # Mostly for consistency with the session-based API
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)

'''

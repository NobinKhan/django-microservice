from django.contrib.auth import get_user_model
from django.utils import timezone

#### all   Rest framework  import ...
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from phonenumber_field.phonenumber import PhoneNumber

from .serializers import RegisterUserSerializer
from .models import OTPtoken, Profile
from functions.handle_error import get_object_or_None


User = get_user_model()


def verify_phone(phone):
    try:
        verified_phone = PhoneNumber.from_string(phone)
        if not verified_phone.is_valid():
            return True, "Invalid Phone Number", status.HTTP_406_NOT_ACCEPTABLE
        return False, verified_phone, None
    except Exception as msg :
        return True, msg.args[0], status.HTTP_406_NOT_ACCEPTABLE


def verify_user(phone):
    user = get_object_or_None(User, phone=phone, username=phone)
    if not user:
        return True, "User Not Found With The Given Phone Number", status.HTTP_404_NOT_FOUND
    return False, user, None


def verify_token(token, user):
    try:
        token = int(token)
    except Exception as msg :
        return True, msg.args[0], status.HTTP_406_NOT_ACCEPTABLE
    otp_obj = get_object_or_None(OTPtoken, token=token, is_active=True)
    if not otp_obj:
        return True, "Invalid OTP Code.", status.HTTP_404_NOT_FOUND
    if otp_obj.type == 'Others':
        otp_obj.is_active = False
        otp_obj.save()
        return False, None, None
    elif otp_obj.type == 'Register' and otp_obj.user.phone == user.phone:
        user.is_active = True
        user.save()
        otp_obj.delete()
        return False, None, None
    elif otp_obj.type == 'Login' and otp_obj.user.phone == user.phone:
        otp_obj.delete()
        return False, None, None
    else:
        return True, "Invalid OTP Code.", status.HTTP_404_NOT_FOUND


def saving_otp_token(type, user=None):
    otp = OTPtoken(type='Login', user=user)
    otp.save()


class Register(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        existing_user = get_object_or_None(User, phone=serializer.validated_data.get('phone'), is_deleted=True)
        if existing_user:
            existing_user.is_deleted = False
            existing_user.save()
            profile = get_object_or_None(Profile, user=existing_user)
            profile.name = serializer.validated_data.get('name')
            profile.save()
            # Sending OTP Code
            saving_otp_token(type='Register', user=existing_user)
        else:
            serializer.save()

        return Response({"message":f"Account created successfully and OTP verification code sent to this {serializer.validated_data.get('phone')} number."}, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        # Storing body data
        token = request.data.get('token')
        phone = request.data.get('phone')
        if not token or not phone:
            return Response({"error":" 'token' and 'phone' field is required. They can't be empty or null."}, status=status.HTTP_404_NOT_FOUND)
        
        error, phone, error_code = verify_phone(phone=phone)
        if error:
            return Response({"error":phone}, status=error_code)
        
        error, user, error_code = verify_user(phone=phone)
        if error:
            return Response({"error":user}, status=error_code)
        
        error, msg, error_code = verify_token(token=token, user=user)
        if error:
            return Response({"error":msg}, status=error_code)
        return Response({
                "refress": "just kidding.",
                "access": "It's a mysterie.",
            }, status=status.HTTP_202_ACCEPTED)


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

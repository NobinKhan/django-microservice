from django.contrib.auth import get_user_model

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
            return Response({"error":"Invalid Phone Number"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return verified_phone
    except Exception as msg :
        return Response({"error":msg.args[0]}, status=status.HTTP_406_NOT_ACCEPTABLE)


def verify_user(phone):
    user = get_object_or_None(User, phone=phone, username=phone)
    if not user:
        return Response({"error":"User Not Found With The Given Phone Number"}, status=status.HTTP_404_NOT_FOUND)
    return user


def verify_token(token, user):
    try:
        token = int(token)
    except Exception as msg :
        return Response({"error":msg.args[0]}, status=status.HTTP_406_NOT_ACCEPTABLE)
    otp_obj = get_object_or_None(OTPtoken, token=token, is_active=True)
    if not otp_obj:
        return Response({"error":"Invalid OTP Code."}, status=status.HTTP_404_NOT_FOUND)
    if otp_obj.type == 'Others':
        otp_obj.is_active = False
        otp_obj.save()
    elif otp_obj.type == 'Register' and otp_obj.user.phone == user.phone:
        user.is_active = True
        user.save()
        otp_obj.delete()
    elif otp_obj.type == 'Login' and otp_obj.user.phone == user.phone:
        otp_obj.delete()
    else:
        return Response({"error":"Invalid OTP Code."}, status=status.HTTP_404_NOT_FOUND)
    return True


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
        
        phone = verify_phone(phone=phone)
        user = verify_user(phone=phone)
        token = verify_token(token=token, user=user)
        print(token)
        if token:
            return Response({
                "refress": "just kidding.",
                "access": "It's a mysterie.",
            }, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"error":"Invalid OTP Code."}, status=status.HTTP_404_NOT_FOUND)


class SendOTP(APIView):
    def get(self, request):
        # Verifying request
        phone = request.query_params.get('phone')
        if not phone:
            return Response({"error":"'phone' param is required. It can't be empty or null."}, status=status.HTTP_404_NOT_FOUND)
        
        phone = verify_phone(phone=phone.replace(" ", "+"))
        user = verify_user(phone=phone)
        if not user.is_deleted:
            return Response({"error":"User Not Found With The Given Phone Number"}, status=status.HTTP_404_NOT_FOUND)

        # Sending OTP Code
        if user.is_active:
            saving_otp_token(type='Login', user=user)
        else:
            saving_otp_token(type='Register', user=user)
        return Response({"message": f"OTP verification code sent to this {user.phone} number."}, status=status.HTTP_202_ACCEPTED)

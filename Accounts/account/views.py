from django.contrib.auth import get_user_model

#### all   Rest framework  import ...
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from phonenumber_field.phonenumber import PhoneNumber

from .serializers import RegisterUserSerializer
from .models import OTPtoken
from functions.handle_error import get_object_or_None


User = get_user_model()

class Register(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        user = serializer.save()

        return Response({"message":f"Account created successfully and OTP verification code sent to this {user.phone} number."}, status=status.HTTP_201_CREATED)


class AccessToken(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')
        otp_phone = request.data.get('phone')
        phone = PhoneNumber.from_string(otp_phone, region='BD')
        user = get_object_or_None(User, phone=phone)
        print(f"in accesstoken phone = {user}")
        print(f"in accesstoken phone = {User.objects.get(username='+8801584613515')}")
        if not user:
            return Response({"message":"User Not Found With The Given Phone Number"}, status=status.HTTP_404_NOT_FOUND)

        # verifying OTP Code
        otp_obj = get_object_or_None(OTPtoken, token=otp_code, is_active=True)
        if not otp_obj:
            return Response({"message":"Invalid OTP Code."}, status=status.HTTP_404_NOT_FOUND)
        if otp_obj.user.phone == user.phone:
            otp_obj.delete()
        elif otp_obj.type == 'Others':
            otp_obj.is_active = False
            otp_obj.save()
        
        # cleaning old data
        old_otp_objs = OTPtoken.objects.filter(user__phone=otp_phone).exclude(token=otp_code)
        if old_otp_objs:
            old_otp_objs.delete()

        return Response(
            {
                "refress": "just kidding.",
                "access": "It's a mysterie.",
            }, status=status.HTTP_202_ACCEPTED)

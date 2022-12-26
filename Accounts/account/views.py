from django.contrib.auth import get_user_model

#### all   Rest framework  import ...
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterUserSerializer
from functions.handle_error import get_object_or_None


User = get_user_model()

class Register(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        user = serializer.save()

        return Response({"message":f"Account created successfully and OTP verification code sent to this {user.phone} number."
                        }, status=status.HTTP_201_CREATED)

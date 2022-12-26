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
        # serializer = RegisterUserSerializer(data=request.data)

        # try:
        #     is_user_available = User.objects.get(Phone = request.data["Phone"])
        # except:
        #     is_user_available = None
        
        # if is_user_available and is_user_available.is_active == True:
        #     return Response({"message": "user with this Phone already exists."}, status=status.HTTP_403_FORBIDDEN)

        # elif is_user_available and is_user_available.is_active == False:
        #     is_user_available.is_active = True
        #     is_user_available.save()
        #     return Response({"message":"User successfully registered, please verify OTP."}, status=status.HTTP_201_CREATED)
        
        return Response({"message":f"{request.data}"}, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
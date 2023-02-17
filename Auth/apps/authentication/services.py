import uuid
from django.contrib.auth import get_user_model

from rest_framework import status
from phonenumber_field.phonenumber import PhoneNumber

from apps.common.utils import get_object
from apps.users.models import OTPtoken

User = get_user_model()


def auth_user_get_jwt_secret_key(user: User) -> str:
    return str(user.jwt_key)


def auth_jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    """
    Default implementation. Add whatever suits you here.
    """
    return {"token": token}


def auth_logout(user: User) -> User:
    user.jwt_key = uuid.uuid4()
    user.full_clean()
    user.save(update_fields=["jwt_key"])

    return user


def verify_phone(phone):
    try:
        verified_phone = PhoneNumber.from_string(phone)
        if not verified_phone.is_valid():
            return True, "Invalid Phone Number", status.HTTP_406_NOT_ACCEPTABLE
        return False, verified_phone, None
    except Exception as msg :
        return True, msg.args[0], status.HTTP_406_NOT_ACCEPTABLE


def verify_user(phone):
    user = get_object(User, phone=phone, username=phone)
    if not user:
        return True, "User Not Found With The Given Phone Number", status.HTTP_404_NOT_FOUND
    return False, user, None


def saving_otp_token(perpose, user=None):
    otp = OTPtoken(perpose=perpose, user=user)
    otp.save()


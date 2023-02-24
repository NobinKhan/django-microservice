from django.urls import include, path

from apps.authentication.apis import (
    SendOTP,
    Login,
    Register,
)

urlpatterns = [
    path("",include(([
        path("register/", Register.as_view(), name="register"),
        path("login/", Login.as_view(), name="login"),
        path("send_otp/", SendOTP.as_view(), name="send_otp")
    ,],"session",)),),

    # path("jwt/",include(([
    #     path("login/", UserJwtLoginApi.as_view(), name="login"),
    #     path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
    # ],"jwt",)),),
    
    # path("me/", UserMeApi.as_view(), name="me"),
]

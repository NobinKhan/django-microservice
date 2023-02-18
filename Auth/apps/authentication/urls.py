from django.urls import include, path

from apps.authentication.apis import (
    Login,
    SendOTP
)

urlpatterns = [
    path("me/", SendOTP.as_view(), name="otp"),
    path("",include(([
        path("login/", Login.as_view(), name="login")
        # path("logout/", UserSessionLogoutApi.as_view(), name="logout")
    ,],"session",)),),

    # path("jwt/",include(([
    #     path("login/", UserJwtLoginApi.as_view(), name="login"),
    #     path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
    # ],"jwt",)),),
    
    # path("me/", UserMeApi.as_view(), name="me"),
]

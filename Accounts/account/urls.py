from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import Register, Login, SendOTP, ServiceQuery


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('send_otp/', SendOTP.as_view(), name='send_otp'),
    path('register/', Register.as_view(), name='register'),
    path('jwt_verify/', TokenVerifyView.as_view(), name='jwt_verify'),
    path('jwt_refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('cheking/', ServiceQuery.as_view(), name='cheking')
]


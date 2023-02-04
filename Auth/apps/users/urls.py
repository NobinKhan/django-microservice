from django.urls import path

from apps.users.apis import UserListApi

urlpatterns = [path("", UserListApi.as_view(), name="list")]

from django.urls import path

from .views import UserListApi


urlpatterns = [path("", UserListApi.as_view(), name="list")]

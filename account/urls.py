
from django.conf.urls import url
from django.urls import path, include
from .api import ChangePasswordView, RegisterApi, UpdateProfileView

urlpatterns = [
    path('api/register', RegisterApi.as_view()),
    path('api/changePassword', ChangePasswordView.as_view()),
    path('api/updateProfile/<int:pk>', UpdateProfileView.as_view()),

]

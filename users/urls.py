from django.urls import path
from .views import StaffSignupAPIView, ClientSignupAPIView, UsersProfileList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("staffsignup/", StaffSignupAPIView.as_view(), name="signup"),
    path("clientsignup/", ClientSignupAPIView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", UsersProfileList.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

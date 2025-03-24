from django.urls import path
from .views import (
    StaffSignupAPIView, 
    ClientSignupAPIView, 
    StaffInvitationList,
    SkillList,
    JobRoleList,
    UniformList
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("staffsignup/", StaffSignupAPIView.as_view(), name="signup"),
    path("clientsignup/", ClientSignupAPIView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("staffinvitation/", StaffInvitationList.as_view(), name="staff_invitation"),
    
    path('api/skills/', SkillList.as_view()),
    path('api/jobroles/', JobRoleList.as_view()),
    path('uniforms/', UniformList.as_view()),

]
# 
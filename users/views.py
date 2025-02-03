from .models import User, StaffInvitation
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    StaffSignupSerializer,
    ClientSignupSerializer,
    UserSerializer,
    StaffInvitationSerializer,
)
from .email_service import send_staff_signup_email, send_client_signup_email, send_staff_invitation_email_from_client


# Create your views here.
class StaffSignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        # invited_user = StaffInvitation.objects.all()
        # print("Invited user", invited_user)
        
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = StaffSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(is_staff=True)

            staff_member = User.objects.get(email=serializer.data["email"])
            # print("user ", staff_member.email)
            send_staff_signup_email(staff_member.email)

            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )

        return Response(data, status=response)


class ClientSignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = ClientSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(is_staff=True)

            staff_member = User.objects.get(email=serializer.data["email"])
            send_client_signup_email(staff_member.email)

            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )

        return Response(data, status=response)


# for invite staff from clinets
class StaffInvitationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        staffInvitation = StaffInvitation.objects.filter(user=request.user)
        serializer = StaffInvitationSerializer(staffInvitation, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StaffInvitationSerializer(data=request.data)
        # print("DFS", request.data['invitations'][0]['staff_email'])
        if serializer.is_valid():
            for invocation in request.data['invitations']:
                staff_email = invocation['staff_email']
                # message = f" {staff_email} {invocation['job_role']} "
                # send_staff_invitation_email_from_client(staff_email, message)

            serializer.save(user=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import User
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import StaffSignupSerializer, ClientSignupSerializer, UserSerializer
from .email_service import send_staff_signup_email, send_client_signup_email

# Create your views here.
class StaffSignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = StaffSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(is_staff = True)

            staff_member = User.objects.get(email=serializer.data["email"])
            send_staff_signup_email(staff_member)

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
            serializer.save(is_staff = True)


            staff_member = User.objects.get(email=serializer.data["email"])
            send_client_signup_email(staff_member)

            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )

        return Response(data, status=response)




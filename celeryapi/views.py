from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.
from .serializers import StaffInfoSerializer
from staff.models import Staff


class StaffToSelery(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        staffs = Staff.objects.all()
        serializer = StaffInfoSerializer(staffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
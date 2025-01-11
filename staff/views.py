from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Staff
)
from .serializers import (
    StaffSerializer,

)

class StaffProfileView(APIView):

    def get(self, request, pk=None):
        if pk is None:
            staff_profiles = Staff.objects.all()
            serializer = StaffSerializer(staff_profiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        staff = Staff.objects.get(pk=pk)
        serializer = StaffSerializer(staff)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff profile created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        staff = Staff.objects.get(pk=pk)
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Staff profile updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
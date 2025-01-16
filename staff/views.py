from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Staff,
    StaffRole
)
from .serializers import (
    StaffSerializer,
    CreateStaffSerializer,
    StaffRoleSerializer

)

class StaffProfileView(APIView):
    def get(self, request, *args, **kwargs):
        staff = Staff.objects.filter(user=request.user).first()
        serializer = StaffSerializer(staff)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = CreateStaffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff profile created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StaffSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Staff profile updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Staff profile deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

class StaffRoleView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = StaffRole.objects.all()
        serializer = StaffRoleSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = StaffRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff role created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
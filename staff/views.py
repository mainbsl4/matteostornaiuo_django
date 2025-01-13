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

class StaffProfileView(generics.ListCreateAPIView):

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
    
